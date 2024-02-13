from typing import Iterable

from utils.routing import CustomAPIRouter


def apply_tags(tags: Iterable[str]):
    """
    Декоратор используется для добавления тегов к роутерам
    """

    def outer(func):
        def inner(*args, **kwargs):
            routers: Iterable[CustomAPIRouter] = func(*args, **kwargs)
            for router in routers:
                router.tags = list(set([*(router.tags or list()), *tags]))
            return routers

        return inner

    return outer
