import os
import json
from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .utillities.shared_state import shared_state
from .utillities.window_manager import window_manager

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "frontend", "dist")

@app.post("/api/window/create")
async def create_window_endpoint(request: dict):
    title = request.get("title", "Nowe Okno")
    # W produkcji nowe okna też otwieramy przez lokalny serwer FastAPI
    window_id = window_manager.create_window(
        title=title,
        url="http://127.0.0.1:8000/"
    )
    return {"window_id": window_id, "status": "created"}

@app.websocket("/ws/{window_id}")
async def websocket_endpoint(websocket: WebSocket, window_id: str):
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