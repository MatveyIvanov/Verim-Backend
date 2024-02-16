import grpc
import logging
import logging.config
from concurrent import futures

import publisher_pb2_grpc
from config import settings
from config.di import Container

from grpc_services import GRPCPublisher
from utils.logging import get_config


def serve():
    # TODO: переписать нормально - через ооп
    Container()
    logging.config.dictConfig(get_config(settings.LOG_PATH))
    print("Publisher gRPC Start Up...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    publisher_pb2_grpc.add_PublisherServicer_to_server(GRPCPublisher(), server)
    server.add_insecure_port(
        f"{settings.PUBLISHER_GRPC_SERVER_HOST}:{settings.PUBLISHER_GRPC_SERVER_PORT}"
    )
    print(
        "Port added..."
    )  # попробовать через лог, uvicorn должен выводить в DEBUG режиме в консоль
    server.start()
    print("Started...")
    print("Waiting for requests...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
