from typing import List

from utils.routing import CustomAPIRouter
from utils.decorators import apply_tags


@apply_tags(("Authorization",))
def get_routers() -> List[CustomAPIRouter]:
    from .registration import router as registration_router
    from .login import router as login_router
    from .jwt import router as jwt_router
    from .password import router as password_router

    return (
        registration_router,
        login_router,
        jwt_router,
        password_router,
    )
