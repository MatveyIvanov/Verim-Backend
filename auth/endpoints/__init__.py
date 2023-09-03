from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from config import celery_app
from config.di import Container


router = APIRouter()


@router.get('/')
@inject
async def test():
    celery_result = celery_app.send_task('config.tasks.divide', args=(1, 2))
    print(celery_result)
    return {'message': 'Testing application'}
