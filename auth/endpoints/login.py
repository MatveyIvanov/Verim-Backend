from dataclasses import asdict

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_versioning import version
from dependency_injector.wiring import Provide, inject

from config.di import Container
from services.login import ILoginUser
from schemas import JWTTokensSchema, LoginSchema
from utils.routing import CustomAPIRouter


router = CustomAPIRouter(prefix="/auth")


@router.post(
    "/login/",
    response_model=JWTTokensSchema,
    status_code=200,
)
@version(1)
@inject
async def login(
    schema: LoginSchema,
    service: ILoginUser = Depends(Provide[Container.login_user]),
):
    return JSONResponse(asdict(service(schema)))
