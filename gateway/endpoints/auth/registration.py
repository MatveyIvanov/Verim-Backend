from dataclasses import asdict

from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi_versioning import version
from dependency_injector.wiring import Provide, inject

from auth_grpc_typed import (
    IAuthStub,
    RegisterRequest,
    RepeatRegisterRequest,
    ConfirmRegisterRequest,
)
from config.di import Container
from schemas import (
    RegistrationSchema,
    JWTTokensSchema,
    CodeSentSchema,
    ConfirmRegistrationSchema,
    RepeatRegistrationCodeSchema,
)
from utils.routing import CustomAPIRouter


router = CustomAPIRouter(prefix="/auth")


@router.post(
    "/register/", response_model=CodeSentSchema, status_code=status.HTTP_201_CREATED
)
@version(1)
@inject
async def register(
    schema: RegistrationSchema,
    auth_grpc: IAuthStub = Depends(Provide[Container.auth_grpc]),
):
    response = await auth_grpc.register(
        request=RegisterRequest(
            email=schema.email,
            username=schema.username,
            password=schema.password,
            re_password=schema.re_password,
        )
    )
    return JSONResponse(
        asdict(CodeSentSchema(email=response.email, message=response.message)),
        status_code=status.HTTP_201_CREATED,
    )


@router.post(
    "/register/repeat-code/",
    response_model=CodeSentSchema,
    status_code=status.HTTP_200_OK,
)
@version(1)
@inject
async def repeat_code(
    schema: RepeatRegistrationCodeSchema,
    auth_grpc: IAuthStub = Depends(Provide[Container.auth_grpc]),
):
    response = await auth_grpc.register_repeat(
        request=RepeatRegisterRequest(email=schema.email)
    )
    return JSONResponse(
        asdict(CodeSentSchema(email=response.email, message=response.message)),
        status_code=status.HTTP_200_OK,
    )


@router.post(
    "/register/confirm/",
    response_model=JWTTokensSchema,
    status_code=status.HTTP_200_OK,
)
@version(1)
@inject
async def register_confirm(
    schema: ConfirmRegistrationSchema,
    auth_grpc: IAuthStub = Depends(Provide[Container.auth_grpc]),
):
    response = await auth_grpc.register_confirm(
        request=ConfirmRegisterRequest(email=schema.email, code=schema.code)
    )
    return JSONResponse(
        asdict(JWTTokensSchema(access=response.access, refresh=response.refresh)),
        status_code=status.HTTP_200_OK,
    )
