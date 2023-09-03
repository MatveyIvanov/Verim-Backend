import os

from fastapi import FastAPI
from celery import Celery


celery = Celery(
    __name__,
    broker=os.environ.get('CELERY_BROKER_URL'),
    backend=os.environ.get('CELERY_RESULT_BACKEND'),
)


@celery.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y


app = FastAPI()


@app.get('/')
async def test():
    divide.delay(1, 2)
    return {'message': 'Testing application'}
