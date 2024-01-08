from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware import Middleware
from fastapi_versioning import version
from dependency_injector.wiring import Provide, inject

from config.di import Container
from services.publications import ICreatePublication
from schemas import PublicationSchema
from utils.middleware import AuthenticationMiddleware
from utils.routing import CustomAPIRouter


router = CustomAPIRouter(prefix="/publications")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    middleware=[Middleware(AuthenticationMiddleware)],
)
@version(1)
@inject
async def create_publication(
    request: Request,
    schema: PublicationSchema,
    service: ICreatePublication = Depends(Provide[Container.create_publication]),
):
    publication = service(request.user, schema)
    return JSONResponse({}, status_code=status.HTTP_201_CREATED)
