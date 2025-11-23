from ..models.api.response import Response, success
from ..consts.messages import *
from typing import Callable


def try_perform_void_action(action: Callable, potential_error_code: int):
    try:
        action()
        return Response(success= success("Action perform success"))
    except Exception as e:
        return Response(error= TYPICAL_ERRORS[potential_error_code])
