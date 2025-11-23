import uuid
import webview
from click.testing import Result

from ..models.api.response import Response, success
from ..consts.messages import *
from backend.models.internal.window import window
from ..utillities.special_functions import *


def generate_window_id(parent: window):
    window_id = f"{parent.title}_{uuid.uuid4()}"
    return window_id

class WindowManager:

    def __init__(self):
        self.windows = list()

    def create_window(self, title: str, url: str, parent: window):

        window_id = generate_window_id(parent)
        config = {
            "title": title,
            "url": f"{url}?window_id={window_id}",
            "width": 800,
            "height": 600,
            "resizable": True
        }

        window_instance = window(title, window_id, parent, config)

        try_perform_void_action(lambda: webview.create_window(**config), 500)


        self.windows.append(window_instance)

        return Response(success= success("Window created successfully!", data={"window_id": window_id}))

    def get_window(self, window_id: str):
        if window_id in [w.window_id for w in self.windows]:
            return Response(success=success("Window successfully found!", data={"window" : next(w.window_id for w in self.windows)}))
        else:
            return Response(error=TYPICAL_ERRORS[404])

    def close_window(self, window_id):
        if window_id in [w.window_id for w in self.windows]:
            self.windows.remove([w.window_id == window_id for w in self.windows])
            return Response(success= success("Successfully removed window."))
        else:
            return Response(error= TYPICAL_ERRORS[404])
        
    def save_to_storage(self, key, value, window_id):
        target_window = next((w for w in self.windows if w.id == window_id), None)
        if target_window:
            target_window.storage[key] = value
            return Response(success= success("Data saved to window storage successfully."))
        else:
            return Response(error= TYPICAL_ERRORS[404])
        
    def get_from_storage(self, key, window_id):
        target_window = next((w for w in self.windows if w.id == window_id), None)
        if target_window:
            value = target_window.storage.get(key, None)
            if value is not None:
                return Response(success= success("Data retrieved from window storage successfully.", data={"value": value}))
            else:
                return Response(error= TYPICAL_ERRORS[404])
        else:
            return Response(error= TYPICAL_ERRORS[404])

    def delete_from_storage(self, key, window_id):
        target_window = next((w for w in self.windows if w.id == window_id), None)
        if target_window:
            if key in target_window.storage:
                del target_window.storage[key]
                return Response(success= success("Data deleted from window storage successfully."))
            else:
                return Response(error= TYPICAL_ERRORS[404])
        else:
            return Response(error= TYPICAL_ERRORS[404])

    def list_windows(self):
        window_list = [{"id": w.window_id, "title": w.title} for w in self.windows]
        return Response(success= success("List of windows retrieved successfully.", data={"windows": window_list}))



window_manager = WindowManager()