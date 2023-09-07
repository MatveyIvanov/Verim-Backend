from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI

from config.di import get_di_container
import endpoints


__app = FastAPI()
__app.container = get_di_container()
for router in endpoints.get_routers():
    __app.include_router(router)
__app = VersionedFastAPI(
    app=__app,
    version_format='{major}',
    prefix_format='/v{major}',
    default_version=(1, 0),
    enable_latest=True
)


def get_fastapi_app() -> FastAPI:
    return __app
