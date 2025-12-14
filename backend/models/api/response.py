from typing import Optional, Any

class error:
    def __init__(self, status_code, details):
        self.status_code = status_code
        self.details = details

    def dict(self):
        return {
            "status_code": self.status_code,
            "details": self.details
        }

class success:
    def __init__(self, message, data: Optional[Any] = None):
        self.status_code = 200
        self.message = message
        self.data = data

    def dict(self):
        result = {
            "status_code": self.status_code,
            "message": self.message
        }
        if self.data is not None:
            result["data"] = self.data
        return result

class Response:
    def __init__(self, success: Optional[success] = None, error: Optional[error] = None):
        self.success = success
        self.error = error

    def dict(self):
        result = {}
        if self.success is not None:
            result["success"] = self.success.dict()
        if self.error is not None:
            result["error"] = self.error.dict()
        return result