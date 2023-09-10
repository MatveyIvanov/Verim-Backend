from dataclasses import asdict

from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from fastapi_versioning import version
from starlette.middleware import Middleware
from dependency_injector.wiring import Provide, inject

from config.di import Container
from services.login import ILoginUser
from schemas import JWTTokensSchema, LoginSchema
from utils.routing import CustomAPIRouter
from utils.middleware import AuthenticationMiddleware


router = CustomAPIRouter(prefix="/auth")


@router.post(
    "/login/",
    response_model=JWTTokensSchema,
    status_code=200,
    middleware=[Middleware(AuthenticationMiddleware)],
)
@version(1)
@inject
async def login(
    schema: LoginSchema,
    request: Request,
    service: ILoginUser = Depends(Provide[Container.login_user]),
):
    print(request.user)
    return JSONResponse(asdict(service(schema)))
