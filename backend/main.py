import os
import json
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.config import undefined
from starlette.websockets import WebSocket
from .models.api.response import Response, success
from .consts.messages import *
from .models.internal.window_model import window_model

# VARIABLES
# VARIABLES
app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "frontend", "dist")

# Import window_manager after app initialization to avoid circular imports
from .utillities.window_manager import window_manager

# WINDOW ENDPOINTS

## create new window
@app.post("/api/window/create")
async def create_window_endpoint(title: str, url: str, parent_id: str = undefined):
    if parent_id is not undefined:
        parent_resp = window_manager.get_window(parent_id)
        if parent_resp.error:
            return parent_resp
    else:
        return Response(error= TYPICAL_ERRORS[ERROR_TYPES.PASSED_PARAMETER_IS_NULL])
    parent: window_model = parent_resp.success.data.window_model

    return await window_manager.create_window(title, url, parent)

## get window by id
@app.get("/api/window/{window_id}")
async def get_window_by_id(window_id: str):
    if window_id not in [w.Id for w in await window_manager.list_windows().success.data.windows]:
        return Response(error= TYPICAL_ERRORS[ERROR_TYPES.WINDOW_NOT_FOUND])
    else:
        return await window_manager.get_window(window_id)

## close window by id
@app.delete("/api/window/{window_id}")
async def close_window(window_id: str):
    if window_id not in [w.Id for w in await window_manager.list_windows()]:
        return Response(error= TYPICAL_ERRORS[ERROR_TYPES.WINDOW_NOT_FOUND])
    else:
        socket_resp = await window_manager.remove_websocket(window_id)
        if socket_resp.error is not undefined:
            return socket_resp
        return await window_manager.close_window(window_id)

## get windows
@app.get("/api/windows")
async def list_windows():
    return window_manager.list_windows()

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