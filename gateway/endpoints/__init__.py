from typing import List

from fastapi import APIRouter


def get_routers() -> List[APIRouter]:
    from .auth.registration import router as registration_router
    from .auth.login import router as login_router
    from .auth.jwt import router as jwt_router
    from .auth.password import router as password_router

    from .publisher.publication import router as publication_router
    from .publisher.vote import router as vote_router

    return (
        registration_router,
        login_router,
        jwt_router,
        password_router,
        publication_router,
        vote_router,
    )
