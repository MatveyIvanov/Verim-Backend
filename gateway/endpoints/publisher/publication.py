from dataclasses import asdict

from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware import Middleware
from fastapi_versioning import version
from fastapi_pagination import Page
from dependency_injector.wiring import Provide, inject

from publisher_pb2 import (
    CreatePublicationRequest,
    PaginationRequest,
)
from config.di import Container
from config.grpc import GRPCHandler
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
    publisher_grpc: GRPCHandler = Depends(Provide[Container.publisher_grpc]),
):
    response = await publisher_grpc(
        "publications_create", CreatePublicationRequest(url=schema.url)
    )
    return JSONResponse(
        asdict(
            PublicationSchema(
                id=response.id,
                url=response.url,
                type=response.type,
                believed_count=response.believed_count,
                disbelieved_count=response.disbelieved_count,
                created_at=response.created_at,
                believed=response.believed,
            )
        ),
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/",
    response_model=Page[PublicationSchema],
    status_code=status.HTTP_200_OK,
    middleware=[Middleware(AuthenticationMiddleware, raise_exception=False)],
)
@version(1)
@inject
async def get_publications(
    request: Request,
    publisher_grpc: GRPCHandler = Depends(Provide[Container.publisher_grpc]),
):
    response = await publisher_grpc("publications_selection", PaginationRequest(page=1))
    return JSONResponse()
