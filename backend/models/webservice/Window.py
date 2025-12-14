from starlette.websockets import WebSocket
from ..internal.window_model import window_model
from webview import Window as pyw

class Window:
    def __init__(self,
                 websocket: WebSocket = None,
                 window_model: window_model = None,
                 pywebview_window: pyw = None):

        self.w = window_model if window_model is not None else window_model()
        self.Id = self.w.id
        self.Websocket = websocket
        self.PyWebViewWindow = pywebview_window

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
        from ...utillities.window_manager import window_manager
        if parent.id not in [w.Id for w in window_manager.windows]:
            raise ValueError("Passed window is not present in the list!")
        self.w.parent = parent

    @property
    def Storage(self):
        return self.w.storage

    @Storage.setter
    def Storage(self, key_value: tuple):
        if key_value is not tuple:
            raise ValueError("Passed argument must be TUPLE( key, value )")
        key, value = key_value
        if value is None:
            self.w.storage.pop(__key= key)
        else:
            self.w.storage[key] = value

    # --- Helper do pobrania całego stanu ---
    def to_dict(self):
        parent_data = None
        if self.Parent is not None:
            parent_data = {
                "window_id": self.Parent.id,
                "title": self.Parent.title
            }

        return {
            "window_id": self.Id,
            "title": self.Title,
            "size": self.Size,
            "url": self.Url,
            "config": self.Config,
            "parent": parent_data,
            "storage": dict(self.Storage) if self.Storage else {},
            "webview_reference": {"id": self.PyWebViewWindow.uid, "title": self.PyWebViewWindow.title }
        }