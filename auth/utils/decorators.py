from functools import wraps

from utils.exceptions import CustomException


def handle_errors(return_class):
    def outer(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except CustomException as e:
                return return_class(detail=e.detail)

        return inner

    return outer
