from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware import Middleware
from fastapi_versioning import version
from dependency_injector.wiring import inject

from utils.middleware import AuthenticationMiddleware
from utils.routing import CustomAPIRouter


router = CustomAPIRouter(prefix="/publications")


@router.post(
    "/",
    status_code=200,
    middleware=[Middleware(AuthenticationMiddleware)]
)
@version(1)
@inject
async def create_publication(request: Request):
    print(request.user)
    return JSONResponse({})
