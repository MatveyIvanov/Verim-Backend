from dataclasses import asdict

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_versioning import version
from dependency_injector.wiring import Provide, inject

from auth_pb2 import LoginRequest
from config.di import Container
from config.grpc import GRPCHandler
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
    schema: LoginSchema, auth_grpc: GRPCHandler = Depends(Provide[Container.auth_grpc])
):
    response = await auth_grpc(
        "login", LoginRequest(login=schema.login, password=schema.password)
    )
    return JSONResponse(
        asdict(JWTTokensSchema(access=response.access, refresh=response.refresh))
    )
