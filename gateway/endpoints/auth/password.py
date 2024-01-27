from dataclasses import asdict

from fastapi import Depends, status, Request
from fastapi.middleware import Middleware
from fastapi.responses import Response, JSONResponse
from fastapi_versioning import version
from dependency_injector.wiring import Provide, inject

from auth_pb2 import (
    ChangePasswordRequest,
    ResetPasswordRequest,
    ResetPasswordConfirmRequest,
)
from config.di import Container
from config.grpc import GRPCHandler
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
    auth_grpc: GRPCHandler = Depends(Provide[Container.auth_grpc]),
):
    await auth_grpc(
        "password_change",
        ChangePasswordRequest(
            user_id=request.user,
            current_password=schema.current_password,
            new_password=schema.new_password,
            re_new_password=schema.re_new_password,
        ),
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/reset-password/", response_model=CodeSentSchema, status_code=status.HTTP_200_OK
)
@version(1)
@inject
async def reset_password(
    schema: ResetPasswordSchema,
    auth_grpc: GRPCHandler = Depends(Provide[Container.auth_grpc]),
):
    response = await auth_grpc(
        "password_reset", ResetPasswordRequest(email=schema.email)
    )
    return JSONResponse(
        asdict(CodeSentSchema(email=response.email, message=response.message)),
        status_code=status.HTTP_200_OK,
    )


@router.post("/reset-password/confirm/", status_code=status.HTTP_200_OK)
@version(1)
@inject
async def reset_password_confirm(
    schema: ResetPasswordConfirmSchema,
    auth_grpc: GRPCHandler = Depends(Provide[Container.auth_grpc]),
):
    await auth_grpc(
        "password_reset_confirm",
        ResetPasswordConfirmRequest(
            email=schema.email,
            code=schema.code,
            new_password=schema.new_password,
            re_new_password=schema.re_new_password,
        ),
    )
    return Response(status_code=status.HTTP_200_OK)
