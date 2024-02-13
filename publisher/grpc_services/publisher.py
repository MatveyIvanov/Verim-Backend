from dependency_injector.wiring import Provide, inject

import publisher_pb2_grpc
from publisher_pb2 import (
    CreatePublicationRequest,
    PublicationResponse,
    VoteRequest,
    PaginationRequest,
    PublicationsSelectionResponse,
)
from auth_pb2 import (
    Empty,
)
from schemas import (
    CreatePublicationSchema,
    PublicationSchema,
    VoteSchema,
)
from config.di import Container
from services.publications import ICreatePublication
from services.votes import IVote
from services.repo import IPublicationRepo
from utils.decorators import handle_errors


class GRPCPublisher(publisher_pb2_grpc.PublisherServicer):
    @handle_errors(PublicationResponse)
    @inject
    def publications_create(
        self,
        request,
        context,
        service: ICreatePublication = Provide[Container.create_publication],
    ):
        publication = service(
            user_id=request.user_id, schema=CreatePublicationSchema(url=request.url)
        )
        return PublicationResponse(
            id=publication.id,
            url=publication.url,
            type=publication.type,
            believed_count=publication.believed_count,
            disbelieved_count=publication.disbelieved_count,
            created_at=publication.created_at,
            believed=None,
        )

    @handle_errors(PublicationsSelectionResponse)
    @inject
    def publications_selection(
        self,
        request,
        context,
        repo: IPublicationRepo = Provide[Container.publication_repo],
    ):
        selection = repo.selection(
            user_id=request.user_id, size=request.size, page=request.page
        )
        return PublicationsSelectionResponse(
            items=[
                PublicationResponse(
                    id=publication.id,
                    url=publication.url,
                    type=publication.type,
                    believed_count=publication.believed_count,
                    disbelieved_count=publication.disbelieved_count,
                    created_at=str(publication.created_at),
                    believed=publication.believed,
                )
                for publication in selection.__dict__["items"]
            ],
            total=selection.__dict__["total"],
            page=selection.__dict__["page"],
            size=selection.__dict__["size"],
            pages=selection.__dict__["pages"],
        )

    @handle_errors(Empty)
    @inject
    def publications_vote(
        self,
        request,
        context,
        service: IVote = Provide[Container.create_vote],
    ):
        service(
            user_id=request.user_id,
            publication_id=request.publication_id,
            schema=VoteSchema(believed=request.believed),
        )
        return Empty()