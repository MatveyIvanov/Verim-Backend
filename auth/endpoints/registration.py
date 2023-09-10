from dataclasses import asdict

from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi_versioning import version
from dependency_injector.wiring import Provide, inject

from config.di import Container
from services.registration import IRegisterUser
from schemas import RegistrationSchema, JWTTokensSchema
from utils.routing import CustomAPIRouter


router = CustomAPIRouter(prefix="/auth")


@router.post("/register/", response_model=JWTTokensSchema, status_code=201)
@version(1)
@inject
async def register(
    schema: RegistrationSchema,
    service: IRegisterUser = Depends(Provide[Container.register_user]),
):
    return JSONResponse(asdict(service(schema)), status_code=status.HTTP_201_CREATED)
