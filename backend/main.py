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
async def websocket_endpoint(window_id: str, websocket: WebSocket = Body()):
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


# EXCERL ENDPOINTS
from .utillities.erxtractor import extractor
@app.get("/extract/excel")
def extract_from_excel_file(excel_file_path:str, key_col_name: str ):

    if os.path.exists(excel_file_path) and os.path.isfile(excel_file_path):

        df: pd.DataFrame = extractor.excel_extractor.extract(excel_file_path, key_col_name)
        data = df.to_dict(orient="records")
        return Response(success=success(f"Excel retrieved successfully! \n path: {excel_file_path}", data= data ))
    
    else:
        return Response(error=TYPICAL_ERRORS[ERROR_TYPES.FILE_NOT_FOUND])

#COMPARE ENDPOINTS
import pandas as pd
from typing import Any
from .utillities.comparator import comparator

@app.post("/compare")
def compare_files(file1: list[dict[str, Any]] = Body(), file1_key: str = Body(), file2: list[dict[str, Any]] = Body(), file2_key: str = Body()):

    if file1 and file2:
        df1 = pd.DataFrame(file1)
        df1.set_index(file1_key)
        df2 = pd.DataFrame(file2)
        df2.set_index(file2_key)

        compare_result: list[dict] | Exception = comparator.compare(df1, df2)

        if isinstance(compare_result, Exception):
            return Response(error=error(ERROR_TYPES.COMPARE_ERROR, str(compare_result)))
        else:
            return Response(success=success("Udało się porównać pliki!", data={"result": compare_result, "is_equal": len(compare_result) == 0}))
    else:
        return Response(error=TYPICAL_ERRORS[ERROR_TYPES.PASSED_PARAMETER_IS_NULL])

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