import uuid
import webview
from starlette.config import undefined
from typing import List
from starlette.websockets import WebSocket, WebSocketState
from backend.models.internal.window_model import window_model
from backend.models.webservice.Window import Window
from ..utillities.special_functions import *


def generate_window_id(parent: window_model | undefined):
    window_id = ""
    if parent == undefined:
        window_id = f"main_{uuid.uuid4()}"
    else:
        window_id = f"{parent.title}_{uuid.uuid4()}"
    return window_id


class WindowManager:

    def __init__(self):
        self.windows: List[Window] = []


    async def create_window(self, title: str, url: str, parent: window_model = undefined):

        print("tworze nowe okno")
        window_id = generate_window_id(parent)
        config = {
            "title": title,
            "url": f"{url}?window_id={window_id}",
            "width": 800,
            "height": 600,
            "resizable": True
        }

        window_instance = Window(window_model = window_model(title, window_id, parent, config))

        window_create_resp = try_perform_void_action(lambda: webview.create_window(**config), ERROR_TYPES.INTERNAL_SERVER_ERROR.value)

        if window_create_resp.error is not undefined:
            return window_create_resp

        self.windows.append(window_instance)

        return Response(success= success("Window created successfully!", data={"window_id": window_id}))

    async def get_window(self, window_id: str):
        if window_id in [w.Id for w in self.windows]:
            return Response(success=success("Window successfully found!", data={"window" : next(w.Id for w in self.windows)}))
        else:
            return Response(error=TYPICAL_ERRORS[ERROR_TYPES.NOT_FOUND])

    async def close_window(self, window_id):
        if window_id in [w.Id for w in self.windows]:
            self.windows.remove(next(w for w in self.windows if w.Id == window_id))
            return Response(success= success("Successfully removed window."))
        else:
            return Response(error= TYPICAL_ERRORS[ERROR_TYPES.NOT_FOUND])
        
    async def save_to_storage(self, key, value, window_id):
        target_window = next((w for w in self.windows if w.Id == window_id), None)
        if target_window:
            target_window.Storage = (key, value)
            return Response(success= success("Data saved to window storage successfully."))
        else:
            return Response(error= TYPICAL_ERRORS[ERROR_TYPES.NOT_FOUND])
        
    async def get_from_storage(self, key, window_id):
        target_window = next((w for w in self.windows if w.Id == window_id), None)
        if target_window:
            value = target_window.Storage.get(key, None)
            if value is not None:
                return Response(success= success("Data retrieved from window storage successfully.", data={"value": value}))
            else:
                return Response(error= TYPICAL_ERRORS[ERROR_TYPES.NOT_FOUND])
        else:
            return Response(error= TYPICAL_ERRORS[ERROR_TYPES.NOT_FOUND])

    async def delete_from_storage(self, key, window_id):
        target_window = next((w for w in self.windows if w.Id == window_id), None)
        if target_window:
            if key in target_window.Storage:
                target_window.Storage = (key, undefined)
                return Response(success= success("Data deleted from window storage successfully."))
            else:
                return Response(error= TYPICAL_ERRORS[ERROR_TYPES.NOT_FOUND])
        else:
            return Response(error= TYPICAL_ERRORS[ERROR_TYPES.NOT_FOUND])

    async def list_windows(self):
        window_list = [{"id": w.Id, "title": w.Title} for w in self.windows]
        return Response(success= success("List of windows retrieved successfully.", data={"windows": window_list}))

    async def register_websocket(self, window_id, websocket: WebSocket):
        if window_id not in [w.Id for w in self.windows]:
            return Response(error= TYPICAL_ERRORS[ERROR_TYPES.WINDOW_NOT_FOUND])

        window = next(w for w in self.windows if w.Id == window_id)
        if window.Websocket is not undefined:
            await window.Websocket.close()
            window.Websocket = undefined

        window.Websocket = websocket
        return Response(success= success("Websocket set successfully!"))

    async def remove_websocket(self, window_id):
        if window_id not in [w.Id for w in self.windows]:
            return Response(error= TYPICAL_ERRORS[ERROR_TYPES.WINDOW_NOT_FOUND])
        window = next(w for w in self.windows if w.Id == window_id)
        if window.Websocket is undefined:
            return Response(error= TYPICAL_ERRORS[ERROR_TYPES.SOCKET_NOT_FOUND])

        await window.Websocket.close()
        window.Websocket = undefined

        return Response(success= success("Successfully closed websocket!"))

    async def send_to_window(self, window_id, payload: str):
        if window_id not in [w.Id for w in self.windows]:
            return Response(error=TYPICAL_ERRORS[ERROR_TYPES.WINDOW_NOT_FOUND])

        window = next(w for w in self.windows if w.Id == window_id)

        if window.Websocket is undefined:
            return Response(error= TYPICAL_ERRORS[ERROR_TYPES.SOCKET_NOT_FOUND])

        if window.Websocket.application_state != WebSocketState.CONNECTED:
            return Response(error= TYPICAL_ERRORS[ERROR_TYPES.WEBSOCKET_IS_CLOSED])

        await window.Websocket.send_text(payload)
        return Response(success= success("Message sent!"))



window_manager = WindowManager()