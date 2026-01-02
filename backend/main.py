import os
import json
from typing import Optional
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Query, Body
from starlette.middleware.cors import CORSMiddleware
from starlette.config import undefined
from starlette.websockets import WebSocket
from pydantic import BaseModel
from .models.api.response import Response, success, error
from .consts.messages import *
from .models.internal.windows.window_model import window_model
from .models.api.pdf_requests import (
    PatternSearchRequestModel,
    PatternMatchResponse,
    PatternExtractionRequest,
    RegionRequest
)
from tkinter import Tk, filedialog
import tempfile

# VARIABLES
# VARIABLES
app = FastAPI()

# CORS Configuration for development mode
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "frontend", "dist")

# Import window_manager after app initialization to avoid circular imports
from .utillities.window_manager import window_manager

# WINDOW ENDPOINTS

## create new window
@app.post("/api/window/create")
async def create_window_endpoint(title: str, url: str, parent_id: Optional[str] = None):
    parent = None
    if parent_id is not None:
        parent_resp = await window_manager.get_window(parent_id)
        if parent_resp.error:
            return parent_resp.dict()
        # Get the actual window object from the manager
        parent_window = next((w for w in window_manager.windows if w.Id == parent_id), None)
        if parent_window:
            parent = parent_window.w 

    result = await window_manager.create_window(title=title, url=url, parent=parent)
    return result.dict()

## get window by id
@app.get("/api/window/{window_id}")
async def get_window_by_id(window_id: str):
    windows_resp = await window_manager.list_windows()
    if window_id not in [w["id"] for w in windows_resp.success.data["windows"]]:
        return Response(error= TYPICAL_ERRORS[ERROR_TYPES.WINDOW_NOT_FOUND]).dict()
    else:
        result = await window_manager.get_window(window_id)
        return result.dict()

## close window by id
@app.delete("/api/window/{window_id}")
async def close_window(window_id: str):
    windows_resp = await window_manager.list_windows()
    windows = [window_model(**w) for w in windows_resp.success.data["windows"]]
    if window_id not in [w.id for w in windows]:
        return Response(error= TYPICAL_ERRORS[ERROR_TYPES.WINDOW_NOT_FOUND]).dict()
    else:
        if any(w.parent and w.parent.id == window_id for w in windows):
            return Response(error= TYPICAL_ERRORS[ERROR_TYPES.WINDOW_CHILDREN_EXISTS])
        socket_resp = await window_manager.remove_websocket(window_id)
        if socket_resp.error is not None:
            return socket_resp.dict()
        result = await window_manager.close_window(window_id)
        return result.dict()

## get windows
@app.get("/api/windows")
async def list_windows():
    result = await window_manager.list_windows()
    return result.dict()

@app.get("/browse/file")
def browse_file():
    root = Tk()
    root.withdraw()  # Ukryj główne okno
    root.attributes('-topmost', True)
    
    file_path = filedialog.askopenfilename(
        title="Wybierz plik Excel",
        filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
    )
    
    root.destroy()
    
    if file_path:
        return {"path": file_path}
    else:
        return {"path": None}

# STORAGE ENDPOINTS

## save data to storage
@app.post("/api/window/{window_id}/storage")
async def save_to_storage(window_id: str, key: str, value: str):
    if window_id not in [w.Id for w in await window_manager.list_windows()]:
        return Response(error= TYPICAL_ERRORS[ERROR_TYPES.WINDOW_NOT_FOUND])
    else:
        return await window_manager.save_to_storage(key, value, window_id)

## get data from storage
@app.get("/api/window/{window_id}/storage")
async def get_from_storage(window_id:str, key: str):
    if window_id not in [w.Id for w in await window_manager.list_windows()]:
        return Response(error= TYPICAL_ERRORS[ERROR_TYPES.WINDOW_NOT_FOUND])
    else:
        return await window_manager.get_from_storage(key, window_id)


## remove from storage
@app.delete("/api/window/{window_id}/storage")
async def remove_from_storage(window_id: str, key: str):
    if window_id not in [w.Id for w in await window_manager.list_windows()]:
        return Response(error= TYPICAL_ERRORS[ERROR_TYPES.WINDOW_NOT_FOUND])
    else:
        return window_manager.delete_from_storage(key, window_id)

# WEBSOCKET ENDPOINTS
## create and operate websocket
@app.websocket("/ws/{window_id}")
async def websocket_endpoint(websocket: WebSocket, window_id: str):
    if window_id not in [w.window_id for w in window_manager.windows]:
        return Response(error= TYPICAL_ERRORS[ERROR_TYPES.WINDOW_NOT_FOUND])

    await websocket.accept()
    await window_manager.register_websocket(window_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message["type"] == "send_to_window":
                target_window = message.get("target")
                payload = message.get("payload")
                if target_window and payload:
                    await window_manager.send_to_window(target_window, payload)
            if message["type"] == "close_connection":
                break

    except Exception as e:
        return Response(error= TYPICAL_ERRORS[ERROR_TYPES.INTERNAL_SERVER_ERROR])

    return await window_manager.remove_websocket(window_id)


# EXCEL ENDPOINTS
from .utillities.extractor import extractor

@app.get("/extract/excel")
def extract_from_excel_file(excel_file_path:str, key_col_name: str ):

    if os.path.exists(excel_file_path) and os.path.isfile(excel_file_path):

        df: pd.DataFrame = extractor.excel_extractor.extract(excel_file_path, key_col_name)
        data = df.to_dict(orient="records")
        return Response(success=success(f"Excel retrieved successfully! \n path: {excel_file_path}", data= data ))
    
    else:
        return Response(error=TYPICAL_ERRORS[ERROR_TYPES.FILE_NOT_FOUND])

@app.get("/extract/excel/columns")
def get_excel_columns(excel_file_path: str):
    
    if os.path.exists(excel_file_path) and os.path.isfile(excel_file_path):

        df: pd.DataFrame = extractor.excel_extractor.extract(excel_file_path)
        return Response(success=success(f"Excel columns! \n path: {excel_file_path}", data= df.columns.tolist() ))
    
    else:
        return Response(error=TYPICAL_ERRORS[ERROR_TYPES.FILE_NOT_FOUND])
    
#COMPARE ENDPOINTS
import pandas as pd
from typing import Any
from .utillities.comparator import comparator
from pydantic import BaseModel

class DuplicateColumnAction(BaseModel):
    column: str
    action: str  # "first", "sum", "custom"
    customValue: str | None = None

class CheckDuplicatesRequest(BaseModel):
    file_path: str
    key_column: str

@app.post("/check-duplicates")
def check_duplicates(request: CheckDuplicatesRequest):
    try:
        df = extractor.excel_extractor.extract(request.file_path)
        df = df.where(pd.notnull(df), None)
        
        duplicated = df.duplicated(subset=[request.key_column], keep=False)
        has_duplicates = duplicated.any()
        duplicate_count = df[duplicated][request.key_column].nunique()
        
        return Response(success=success("Sprawdzono", data={
            "has_duplicates": bool(has_duplicates),
            "duplicate_keys_count": int(duplicate_count)
        }))
    except Exception as e:
        return Response(error=error(ERROR_TYPES.COMPARE_ERROR, str(e)))


class ColumnPair(BaseModel):
    file1Column: str
    file2Column: str

class CompareRequest(BaseModel):
    file1_path: str
    file1_key_column: str
    file1_duplicate_actions: list[DuplicateColumnAction] = []
    file2_path: str
    file2_key_column: str
    file2_duplicate_actions: list[DuplicateColumnAction] = []
    column_pairs: list[ColumnPair]

def values_equal(val1, val2, tolerance=0.01):
    """Porównuje wartości z tolerancją dla floatów"""
    if val1 is None and val2 is None:
        return True
    if val1 is None or val2 is None:
        return False
    
    try:
        f1 = float(val1)
        f2 = float(val2)
        return abs(f1 - f2) < tolerance
    except (ValueError, TypeError):
        return val1 == val2

def format_value(val):
    """Zaokrągla floaty do 2 miejsc po przecinku"""
    if val is None:
        return None
    try:
        f = float(val)
        return round(f, 2)
    except (ValueError, TypeError):
        return val

def resolve_duplicates(df: pd.DataFrame, key_column: str, actions: list[DuplicateColumnAction]) -> pd.DataFrame:
    """Scala duplikaty według globalnej konfiguracji"""
    
    action_map = {a.column: a for a in actions}
    result_rows = []
    
    for key, group in df.groupby(key_column):
        if len(group) == 1:
            result_rows.append(group.iloc[0].to_dict())
            continue
        
        row = {key_column: key}
        
        for col in df.columns:
            if col == key_column:
                continue
            
            action_config = action_map.get(col)
            action = action_config.action if action_config else "first"
            custom_value = action_config.customValue if action_config else None
            
            if action == "first":
                row[col] = group.iloc[0][col]
            elif action == "last":
                row[col] = group.iloc[-1][col]
            elif action == "min":
                try:
                    row[col] = group[col].min()
                except:
                    row[col] = group.iloc[0][col]
            elif action == "max":
                try:
                    row[col] = group[col].max()
                except:
                    row[col] = group.iloc[0][col]
            elif action == "sum":
                try:
                    total = group[col].sum()
                    row[col] = round(total, 2) if isinstance(total, float) else total
                except:
                    row[col] = group.iloc[0][col]
            elif action == "custom":
                row[col] = custom_value
        
        result_rows.append(row)
    
    return pd.DataFrame(result_rows)

@app.post("/compare")
def compare_files(request: CompareRequest):
    try:
        # Wczytaj pliki
        df1 = extractor.excel_extractor.extract(request.file1_path)
        df1 = df1.where(pd.notnull(df1), None)
        
        df2 = extractor.excel_extractor.extract(request.file2_path)
        df2 = df2.where(pd.notnull(df2), None)
        
        # Rozwiąż duplikaty
        if request.file1_duplicate_actions:
            df1 = resolve_duplicates(df1, request.file1_key_column, request.file1_duplicate_actions)
        
        if request.file2_duplicate_actions:
            df2 = resolve_duplicates(df2, request.file2_key_column, request.file2_duplicate_actions)
        
        # Ustaw klucze jako index
        df1 = df1.set_index(request.file1_key_column)
        df2 = df2.set_index(request.file2_key_column)
        
        # Porównaj wspólne klucze
        common_keys = df1.index.intersection(df2.index)
        
        differences = []
        for key in common_keys:
            for pair in request.column_pairs:
                val1 = df1.loc[key, pair.file1Column]
                val2 = df2.loc[key, pair.file2Column]
                
                # Użyj tolerancji przy porównywaniu
                if not values_equal(val1, val2):
                    differences.append({
                        "key": str(key),
                        "column": f"{pair.file1Column} / {pair.file2Column}",
                        "value1": format_value(val1),
                        "value2": format_value(val2)
                    })
        
        return Response(success=success("Porównano!", data={
            "result": differences,
            "is_equal": len(differences) == 0
        }))
        
    except Exception as e:
        return Response(error=error(ERROR_TYPES.COMPARE_ERROR, str(e)))
    

# STATIC FILES
## get asset by path
if os.path.exists(DIST_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(DIST_DIR, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        file_path = os.path.join(DIST_DIR, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)

        return FileResponse(os.path.join(DIST_DIR, "index.html"))
else:
    print(f"UWAGA: Nie znaleziono folderu {DIST_DIR}. Uruchom 'npm run build' w folderze frontend.")