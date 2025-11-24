
from ..models.api.response import error
from enum import Enum
# FAST API response messages

class ERROR_TYPES(Enum):
    NOT_FOUND = 404,
    INTERNAL_SERVER_ERROR = 505,
    WINDOW_NOT_FOUND = 4000,
    PASSED_PARAMETER_IS_NULL = 4001,
    SOCKET_NOT_FOUND = 4002

TYPICAL_ERRORS = dict({
    ERROR_TYPES.NOT_FOUND: error(ERROR_TYPES.NOT_FOUND.value, "Element you are looking for doesn't exists!"),
    ERROR_TYPES.INTERNAL_SERVER_ERROR: error(ERROR_TYPES.INTERNAL_SERVER_ERROR.value, "Something Went Wrong!"),
    ERROR_TYPES.WINDOW_NOT_FOUND: error(ERROR_TYPES.WINDOW_NOT_FOUND.value, "Window for passed id not found!"),
    ERROR_TYPES.PASSED_PARAMETER_IS_NULL: error(ERROR_TYPES.PASSED_PARAMETER_IS_NULL.value, "Passed parameter cannot be null!"),
    ERROR_TYPES.SOCKET_NOT_FOUND: error(ERROR_TYPES.SOCKET_NOT_FOUND.value, "Socket you are looking for doesn't exist")
})


