
from ..models.api.response import error
from enum import Enum
# FAST API response messages

class ERROR_TYPES(Enum):
    NOT_FOUND = 404,
    INTERNAL_SERVER_ERROR = 505,
    WINDOW_NOT_FOUND = 4000,
    PASSED_PARAMETER_IS_NULL = 4001,
    SOCKET_NOT_FOUND = 4002,
    WEBSOCKET_IS_CLOSED = 5000,
    WINDOW_CHILDREN_EXISTS = 5001,
    FILE_NOT_FOUND = 4004,
    COMPARE_ERROR = 5005

TYPICAL_ERRORS = dict({
    ERROR_TYPES.NOT_FOUND: error(ERROR_TYPES.NOT_FOUND.value, "Element you are looking for doesn't exists!"),
    ERROR_TYPES.INTERNAL_SERVER_ERROR: error(ERROR_TYPES.INTERNAL_SERVER_ERROR.value, "Something Went Wrong!"),
    ERROR_TYPES.WINDOW_NOT_FOUND: error(ERROR_TYPES.WINDOW_NOT_FOUND.value, "Window for passed id not found!"),
    ERROR_TYPES.PASSED_PARAMETER_IS_NULL: error(ERROR_TYPES.PASSED_PARAMETER_IS_NULL.value, "Passed parameter cannot be null!"),
    ERROR_TYPES.SOCKET_NOT_FOUND: error(ERROR_TYPES.SOCKET_NOT_FOUND.value, "Socket you are looking for doesn't exist"),
    ERROR_TYPES.WEBSOCKET_IS_CLOSED: error(ERROR_TYPES.WEBSOCKET_IS_CLOSED.value, "Socket you are looking for is closed"),
    ERROR_TYPES.WINDOW_CHILDREN_EXISTS: error(ERROR_TYPES.WINDOW_CHILDREN_EXISTS.value, "Before you delete main window you should first close all children windows!"),
    ERROR_TYPES.FILE_NOT_FOUND: error(ERROR_TYPES.FILE_NOT_FOUND.value, "File you are looking for doesn't exists!"),
    ERROR_TYPES.COMPARE_ERROR: error(ERROR_TYPES.COMPARE_ERROR.value, "During compare there was an error!")
})


