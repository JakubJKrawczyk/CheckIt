from pydantic.v1.schema import model_schema
from starlette.config import undefined

class window:
    def __init__(
            self,
            title = undefined,
            id = undefined,
            parent = undefined,
            size = (0,0),
            config = undefined,
            url = undefined
            ):
        self.title = title
        self.id = id
        self.size = size
        self.parent = parent
        self.url = url
        self.config = config


