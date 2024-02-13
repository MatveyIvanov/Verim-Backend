from dataclasses import asdict

from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware import Middleware
from fastapi_versioning import version
from fastapi_pagination import Page
from dependency_injector.wiring import Provide, inject

from publisher_grpc_typed import (
    IPublisherStub,
    CreatePublicationRequest,
    PaginationRequest,
)
from config.di import Container
from schemas import (
    CreatePublicationSchema,
    PublicationSchema,
    PublicationSelectionSchema,
)
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
    publisher_grpc: IPublisherStub = Depends(Provide[Container.publisher_grpc]),
):
    response = await publisher_grpc.publications_create(
        request=CreatePublicationRequest(user_id=request.user, url=str(schema.url))
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
    publisher_grpc: IPublisherStub = Depends(Provide[Container.publisher_grpc]),
):
    page = request.query_params.get("page", None)
    size = request.query_params.get("size", None)
    if page:
        page = int(page)
    if size:
        size = int(size)
    response = await publisher_grpc.publications_selection(
        request=PaginationRequest(
            user_id=request.user,
            page=page,
            size=size,
        )
    )
    return JSONResponse(
        asdict(
            PublicationSelectionSchema(
                items=[
                    PublicationSchema(
                        id=publication.id,
                        url=publication.url,
                        type=publication.type,
                        believed_count=publication.believed_count,
                        disbelieved_count=publication.disbelieved_count,
                        created_at=publication.created_at,
                        believed=publication.believed,
                    )
                    for publication in response.items
                ],
                total=response.total,
                page=response.page,
                size=response.size,
                pages=response.pages,
            )
        )
    )
