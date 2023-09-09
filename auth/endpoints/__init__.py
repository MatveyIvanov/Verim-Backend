from typing import List

from fastapi import APIRouter

from .registration import router as registration_router
from .login import router as login_router


def get_routers() -> List[APIRouter]:
    return (registration_router, login_router)
