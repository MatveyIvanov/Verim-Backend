from typing import List

from utils.routing import CustomAPIRouter


def get_routers() -> List[CustomAPIRouter]:
    from .auth import get_routers as get_auth_routers
    from .publisher import get_routers as get_publisher_routers

    return (
        *get_auth_routers(),
        *get_publisher_routers(),
    )
