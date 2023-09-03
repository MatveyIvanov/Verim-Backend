from fastapi import FastAPI

from config.di import get_di_container
import endpoints


__app = FastAPI()
__app.container = get_di_container()
__app.include_router(endpoints.router)


def get_fastapi_app() -> FastAPI:
    return __app
