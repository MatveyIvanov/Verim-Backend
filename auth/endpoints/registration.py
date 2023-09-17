from dataclasses import asdict

from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi_versioning import version
from dependency_injector.wiring import Provide, inject

from config.di import Container
from services.registration import IRegisterUser, IConfirmRegistration
from schemas import (
    RegistrationSchema,
    JWTTokensSchema,
    CodeSentSchema,
    ConfirmRegistrationSchema,
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
    service: IRegisterUser = Depends(Provide[Container.register_user]),
):
    return JSONResponse(asdict(service(schema)), status_code=status.HTTP_201_CREATED)


@router.post(
    "/register/confirm/",
    response_model=JWTTokensSchema,
    status_code=status.HTTP_200_OK,
)
@version(1)
@inject
async def register_confirm(
    schema: ConfirmRegistrationSchema,
    service: IConfirmRegistration = Depends(Provide[Container]),
):
    return JSONResponse(asdict(service()), status.HTTP_200_OK)
