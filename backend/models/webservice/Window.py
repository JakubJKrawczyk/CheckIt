from starlette.config import undefined
from ..internal.window import  window


class Window:
    def __init__(self,

                 window_model = undefined):

        self.w = window_model if window_model is not undefined else window()
        self.Id = window.id



