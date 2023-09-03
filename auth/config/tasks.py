from __future__ import absolute_import

from config import celery_app


@celery_app.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y
