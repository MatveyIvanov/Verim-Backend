from dataclasses import asdict

from fastapi import Depends, status, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi_versioning import version
from dependency_injector.wiring import Provide, inject

from config.di import Container
from config.mail import ISendEmail, SendEmailEntry
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


@router.post(
    "/register/confirm/",
    response_model=JWTTokensSchema,
    status_code=status.HTTP_201_CREATED,
)
@version(1)
@inject
async def register_confirm(
    background_tasks: BackgroundTasks,
    service: ISendEmail = Depends(Provide[Container.send_email]),
):
    background_tasks.add_task(
        service,
        entry=SendEmailEntry(
            emails=["cool.matvey250301@gmail.com"],
            subject="Test",
            message="Test test test",
        ),
    )
    return JSONResponse({}, status.HTTP_201_CREATED)
