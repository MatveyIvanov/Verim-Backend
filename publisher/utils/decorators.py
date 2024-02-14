from typing import Iterable

from sqlalchemy.exc import SQLAlchemyError

from utils.exceptions import CustomException, Custom400Exception


def handle_errors(return_class):
    def outer(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except CustomException as e:
                return return_class(detail=e.detail)

        return inner

    return outer


def handle_grpc_response_error(func):
    async def wrapper(*args, **kwargs):
        response = await func(*args, **kwargs)
        if getattr(response, "detail", None):
            raise Custom400Exception(detail=response.detail)
        return response

    return wrapper


def apply_tags(tags: Iterable[str]):
    """
    Декоратор используется для добавления тегов к роутерам
    """

    def outer(func):
        def inner(*args, **kwargs):
            routers = func(*args, **kwargs)
            for router in routers:
                router.tags = list(set([*(router.tags or list()), *tags]))
            return routers

        return inner

    return outer


def handle_orm_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            # TODO: logging
            raise e

    return wrapper
