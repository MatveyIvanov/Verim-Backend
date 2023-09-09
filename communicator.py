import requests
import json
from typing import Dict
from abc import ABC, abstractmethod


class IMicroserviceCommunicator(ABC):
    @abstractmethod
    def __init__(self, microservice_name: str, endpoint: str, data: Dict) -> None:
        ...

    @abstractmethod
    def communicate(self) -> Dict:
        ...


class MicroserviceCommunicator(IMicroserviceCommunicator):
    MICROSERVICE_PORT_MAP = {
        "auth": 8000,
    }
    SUPPORTED_HTTP_METHODS = ("get", "post", "put", "patch", "delete")

    def __init__(
        self, microservice_name: str, method: str, endpoint: str, data: Dict
    ) -> None:
        method = method.lower()

        assert (
            microservice_name in self.MICROSERVICE_PORT_MAP.keys()
        ), f"Unsupported microservice name - {microservice_name}"
        assert method in self.SUPPORTED_HTTP_METHODS, f"Unsupported method - {method}"

        self.microservice_name = microservice_name
        self.method = method
        self.endpoint = endpoint
        self.data = data

    def communicate(self) -> Dict:
        return json.loads(
            s=getattr(requests, self.method)(
                url=self._build_path(), data=json.dumps(self.data)
            )
        )

    def _build_path(self):
        return f'http://127.0.0.1:{self.MICROSERVICE_PORT_MAP.get()}/{self.endpoint.strip("/")}/'
