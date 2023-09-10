from dataclasses import asdict

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_versioning import version
from dependency_injector.wiring import Provide, inject

from config.di import Container
from services.jwt import IRefreshJWTTokens
from schemas import JWTTokensSchema, RefreshTokensSchema
from utils.routing import CustomAPIRouter


router = CustomAPIRouter(prefix="/auth/jwt")


@router.post(
    "/refresh/",
    response_model=JWTTokensSchema,
    status_code=200,
)
@version(1)
@inject
async def refresh(
    schema: RefreshTokensSchema,
    service: IRefreshJWTTokens = Depends(Provide[Container.refresh_jwt_tokens]),
):
    return JSONResponse(asdict(service(schema)))
