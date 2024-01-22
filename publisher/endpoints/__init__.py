from typing import List

from fastapi import APIRouter


def get_routers() -> List[APIRouter]:
    from .publication import router as publication_router
    from .vote import router as vote_router

    return (publication_router, vote_router)
