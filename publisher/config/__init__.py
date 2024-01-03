from config.celery import app as celery_app


__all__ = ("celery_app",)

# TODO: когда будет готово хотя бы 2 микросервиса, посмотреть,
# можно ли вынести что-то из конфига и маунтить для каждого микросервиса
# через docker-compose.yml
