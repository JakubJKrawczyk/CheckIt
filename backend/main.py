import os
import json
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

from .utillities.shared_state import shared_state
from .utillities.window_manager import window_manager

app = FastAPI()

@app.post("/api/window/create")
async def create_window_endpoint(request: dict):
    title = request.get("title", "Nowe Okno")
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

app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")