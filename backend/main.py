import os
import json
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.config import undefined
from .models.api.response import Response
from .utillities.shared_state import shared_state
from .utillities.window_manager import window_manager
from .consts.messages import *
from .models.internal.window_model import window_model

# VARIABLES
app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "frontend", "dist")


# WINDOW ENDPOINTS
@app.post("/api/window/create")
async def create_window_endpoint(title: str, url: str, parent_id: str = undefined):
    if parent_id is not undefined:
        parent_resp = window_manager.get_window(parent_id)
        if parent_resp.error:
            return parent_resp
    else:
        return Response(error= TYPICAL_ERRORS[ERROR_TYPES.PASSED_PARAMETER_IS_NULL])
    parent: window_model = parent_resp.success.data.window_model

    resp = window_manager.create_window(title, url, parent)
    return resp

@app.websocket("/ws/{window_id}")
async def websocket_endpoint(websocket: WebSocket, window_id: str):
    if window_id not in [w.window_id for w in window_manager.windows]:
        return Response(error= TYPICAL_ERRORS[ERROR_TYPES.WINDOW_NOT_FOUND])

    await websocket.accept()
    await shared_state.add_subscriber(window_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message["type"] == "send_to_window":
                target_window = message.get("target")
                payload = message.get("payload")
                if target_window and payload:
                    await shared_state.send_to_window(target_window, payload)
    except Exception:
        pass
    finally:
        await shared_state.remove_subscriber(window_id)

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