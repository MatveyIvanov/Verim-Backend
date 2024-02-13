import grpc
from concurrent import futures

import auth_pb2_grpc
from config import settings
from config.di import Container
from grpc_services import GRPCAuth


def serve():
    Container()
    print("Auth GRPC Start Up...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServicer_to_server(GRPCAuth(), server)
    server.add_insecure_port(
        f"{settings.AUTH_GRPC_SERVER_HOST}:{settings.AUTH_GRPC_SERVER_PORT}"
    )
    print("Port added...")
    server.start()
    print("Started...")
    print("Waiting for requests...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
