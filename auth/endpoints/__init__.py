from typing import List

from fastapi import APIRouter

from .registration import router as registration_router


def get_routers() -> List[APIRouter]:
    return (registration_router,)
