from dataclasses import asdict

from fastapi import Depends, status, Request
from fastapi.middleware import Middleware
from fastapi.responses import Response, JSONResponse
from fastapi_versioning import version
from dependency_injector.wiring import Provide, inject

from config.di import Container
from services.password import IChangePassword, IResetPassword
from schemas import (
    ChangePasswordSchema,
    CodeSentSchema,
    ResetPasswordSchema,
    ResetPasswordConfirmSchema,
)
from utils.middleware import AuthenticationMiddleware
from utils.routing import CustomAPIRouter


router = CustomAPIRouter(prefix="/auth")


@router.post(
    "/change-password/",
    status_code=status.HTTP_204_NO_CONTENT,
    middleware=[Middleware(AuthenticationMiddleware)],
)
@version(1)
@inject
async def change_password(
    request: Request,
    schema: ChangePasswordSchema,
    service: IChangePassword = Depends(Provide[Container.change_password]),
):
    service(request.user, schema)
    return Response(status.HTTP_204_NO_CONTENT)


@router.post(
    "/reset-password/", response_model=CodeSentSchema, status_code=status.HTTP_200_OK
)
@version(1)
@inject
async def reset_password(
    schema: ResetPasswordSchema,
    service: IResetPassword = Depends(Provide[Container.reset_password]),
):
    return JSONResponse(asdict(service(schema)), status_code=status.HTTP_200_OK)


@router.post("/reset-password/confirm/", status_code=status.HTTP_200_OK)
@version(1)
@inject
async def reset_password_confirm(
    schema: ResetPasswordConfirmSchema,
    service: IResetPassword = Depends(Provide[Container.confirm_reset_password]),
):
    service(schema)
    return Response(status_code=status.HTTP_200_OK)
