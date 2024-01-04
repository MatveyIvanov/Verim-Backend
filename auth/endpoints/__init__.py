from typing import List

from fastapi import APIRouter


def get_routers() -> List[APIRouter]:
    from .registration import router as registration_router
    from .login import router as login_router
    from .jwt import router as jwt_router
    from .password import router as password_router

    return (registration_router, login_router, jwt_router, password_router)
