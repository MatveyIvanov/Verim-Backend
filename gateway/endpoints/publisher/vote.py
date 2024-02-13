from fastapi import Depends, status
from fastapi.responses import Response
from fastapi.requests import Request
from fastapi.middleware import Middleware
from fastapi_versioning import version
from dependency_injector.wiring import Provide, inject

from publisher_grpc_typed import IPublisherStub, VoteRequest
from config.di import Container
from schemas import VoteSchema
from utils.middleware import AuthenticationMiddleware
from utils.routing import CustomAPIRouter


router = CustomAPIRouter(prefix="/publications/{publication_id}")


@router.post(
    "/vote/",
    status_code=status.HTTP_200_OK,
    middleware=[Middleware(AuthenticationMiddleware)],
)
@version(1)
@inject
async def vote(
    request: Request,
    schema: VoteSchema,
    publication_id: int,
    publisher_grpc: IPublisherStub = Depends(Provide[Container.publisher_grpc]),
):
    await publisher_grpc.publications_vote(
        request=VoteRequest(
            user_id=request.user,
            publication_id=publication_id,
            believed=schema.believed,
        )
    )
    return Response()
