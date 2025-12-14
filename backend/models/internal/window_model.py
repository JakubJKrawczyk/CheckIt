from pydantic.v1.schema import model_schema

class window_model:
    def __init__(
            self,
            title = None,
            id = None,
            parent = None,
            size = (0,0),
            config = None,
            url = None
            ):
        self.title = title
        self.id = id
        self.size = size
        self.parent = parent
        self.url = url
        self.config = config
        self.storage = dict()


