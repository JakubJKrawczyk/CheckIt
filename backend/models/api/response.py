from starlette.config import undefined

class error:
    def __init__(self, status_code, details):
        self.status_code = status_code
        self.details = details

class success:
    def __init__(self, message, data = undefined):
        self.status_code = 200
        self.message = message
        self.data = data

class Response:
    def __init__(self, success: success = undefined, error: error = undefined):
        self.success = success
        self.error = error