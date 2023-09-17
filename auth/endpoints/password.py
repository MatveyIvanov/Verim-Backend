from fastapi import Depends, status, Request
from fastapi.middleware import Middleware
from fastapi.responses import JSONResponse
from fastapi_versioning import version
from dependency_injector.wiring import Provide, inject

from config.di import Container
from services.password import IChangePassword
from schemas import ChangePasswordSchema
from utils.middleware import AuthenticationMiddleware
from utils.routing import CustomAPIRouter


router = CustomAPIRouter(prefix="/auth")


@router.post(
    "/change-password/",
    response_model=None,
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
    return JSONResponse(None, status.HTTP_204_NO_CONTENT)
