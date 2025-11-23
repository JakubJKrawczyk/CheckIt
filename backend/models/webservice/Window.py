from starlette.websockets import WebSocket
from starlette.config import undefined
from ..internal.window_model import window_model
from ...utillities.window_manager import WindowManager, window_manager


class Window:
    def __init__(self,
                 websocket: WebSocket = undefined,
                 window_model: window_model = undefined):

        self.w = window_model if window_model is not undefined else window_model()
        self.Id = self.w.id
        self.Websocket = websocket

    # --- Title ---
    @property
    def Title(self):
        return self.w.title

    @Title.setter
    def Title(self, title: str):
        if not title:
            raise ValueError("Title can't be empty")
        self.w.title = title

    # --- Size ---
    @property
    def Size(self):
        return self.w.size

    @Size.setter
    def Size(self, size):
        if not isinstance(size, (tuple, list)) or len(size) != 2:
            raise ValueError("Size must be a tuple or list of 2 values (width, height)")
        self.w.size = size

    # --- Url ---
    @property
    def Url(self):
        return self.w.url

    @Url.setter
    def Url(self, url: str):
        self.w.url = url

    # --- Config ---
    @property
    def Config(self):
        return self.w.config

    @Config.setter
    def Config(self, config: dict):
        if not isinstance(config, dict):
            raise ValueError("Config must be a dictionary")
        self.w.config = config

    @property
    def Parent(self):
        return self.w.parent

    @Parent.setter
    def Parent(self, parent: window_model):
        if parent.id not in [w.window_id for w in window_manager.list_windows()]:
            raise ValueError("Passed window is not presentent in tle list!")
        self.w.parent = parent

    @property
    def Storage(self):
        return self.w.storage

    @Storage.setter
    def Storage(self, key_value: tuple):
        if key_value is not tuple:
            raise ValueError("Passed argument must be TUPLE( key, value )")
        key, value = key_value
        if value is undefined:
            self.w.storage.pop(__key= key)
        else:
            self.w.storage[key] = value

    # --- Helper do pobrania całego stanu ---
    def to_dict(self):
        return {
            "id": self.Id,
            "title": self.Title,
            "size": self.Size,
            "url": self.Url,
            "config": self.Config,
            "parent": self.Parent,
            "storage": self.Storage
        }