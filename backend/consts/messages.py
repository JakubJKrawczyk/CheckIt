
from ..models.api.response import error
# FAST API response messages

TYPICAL_ERRORS = dict({
    404: error(404, "Element you are looking for doesn't exists!"),
    500: error(500, "Something Went Wrong!")
})