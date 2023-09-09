from dataclasses import asdict

from fastapi import APIRouter, Depends
from fastapi_versioning import version
from dependency_injector.wiring import Provide, inject

from config.di import Container
from services.regisration import IRegisterUser
from schemas.register import RegistrationSchema, JWTTokensSchema


router = APIRouter(prefix="/auth")


@router.post("/register/", response_model=JWTTokensSchema, status_code=201)
@version(1)
@inject
async def register(
    schema: RegistrationSchema,
    service: IRegisterUser = Depends(Provide[Container.register_user]),
):
    tokens = service(schema)

    return asdict(tokens)
