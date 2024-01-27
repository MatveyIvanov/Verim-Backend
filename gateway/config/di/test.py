from dependency_injector import containers, providers

from config.di.dev import Container


@containers.copy(Container)
class TestContainer(containers.DeclarativeContainer):
    pass
