from typing import TypeVar, Generic

from fastapi.responses import JSONResponse
import grpc

from utils.exceptions import Custom400Exception


T = TypeVar("T")


class GRPCConnection(Generic[T]):
    """Class responsible for initializing grpc channel at startup"""

    def __init__(self, host: str, port: int, stub: T):
        """Init a channel"""
        self.channel = grpc.aio.insecure_channel(f"{host}:{port}")
        self.stub = stub(self.channel)

    def __call__(self) -> T:
        """Get a stub to use for the grpc"""
        return self.stub


class GRPCHandler:
    def __init__(self, grpc_conn: GRPCConnection) -> None:
        self.grpc_conn = grpc_conn

    async def __call__(self, method: str, request):
        connection = self.grpc_conn()
        assert hasattr(connection, method), "Bad method"
        response = await getattr(connection, method)(request)
        if getattr(response, "detail", None):
            raise Custom400Exception(detail=response.detail)
        return response
