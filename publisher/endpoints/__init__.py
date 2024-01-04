from typing import List

from fastapi import APIRouter


def get_routers() -> List[APIRouter]:
    from .publication import router as publication_router
    return (publication_router,)
