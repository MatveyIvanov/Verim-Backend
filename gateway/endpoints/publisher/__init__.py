from typing import List

from utils.routing import CustomAPIRouter
from utils.decorators import apply_tags


@apply_tags(("Publications",))
def get_routers() -> List[CustomAPIRouter]:
    from .publication import router as publication_router
    from .vote import router as vote_router

    return (
        publication_router,
        vote_router,
    )
