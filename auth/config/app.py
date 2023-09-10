from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi_versioning import VersionedFastAPI

from config.di import get_di_container
import endpoints
from utils.middleware import AuthenticationMiddleware
from utils.app import CustomFastAPI


container = get_di_container()


db = container.db()
db.create_database()


__app = CustomFastAPI()
__app.container = container
for router in endpoints.get_routers():
    __app.include_router(router)
__app.router
__app = VersionedFastAPI(
    app=__app,
    version_format="{major}",
    prefix_format="/api/v{major}",
    default_version=(1, 0),
    enable_latest=True,
)
# __app.add_middleware(HTTPSRedirectMiddleware)  # FIXME for production
__app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])  # FIXME for production


def get_fastapi_app() -> CustomFastAPI:
    return __app
