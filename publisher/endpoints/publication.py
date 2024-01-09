from dataclasses import asdict

from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware import Middleware
from fastapi_versioning import version
from fastapi_pagination import Page
from dependency_injector.wiring import Provide, inject

from config.di import Container
from services.publications import ICreatePublication
from services.repo import IPublicationRepo
from schemas import CreatePublicationSchema, PublicationSchema
from utils.middleware import AuthenticationMiddleware
from utils.routing import CustomAPIRouter


router = CustomAPIRouter(prefix="/publications")


@router.post(
    "/",
    response_model=PublicationSchema,
    status_code=status.HTTP_201_CREATED,
    middleware=[Middleware(AuthenticationMiddleware)],
)
@version(1)
@inject
async def create_publication(
    request: Request,
    schema: CreatePublicationSchema,
    service: ICreatePublication = Depends(Provide[Container.create_publication]),
):
    return JSONResponse(
        asdict(service(request.user, schema)), status_code=status.HTTP_201_CREATED
    )


@router.get(
    "/",
    response_model=Page[PublicationSchema],
    status_code=status.HTTP_200_OK,
    middleware=[Middleware(AuthenticationMiddleware)],
)
@version(1)
@inject
async def get_publications(
    request: Request,
    repo: IPublicationRepo = Depends(Provide[Container.publication_repo]),
):
    return repo.selection(request.user)
