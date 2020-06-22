from abc import abstractmethod, ABCMeta
from typing import List


class ProviderInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_credentials(self) -> None:
        raise NotImplementedError("get_credentials method is not implemented!")

    @abstractmethod
    def publish(self, topic: str, data, **kwargs) -> None:
        raise NotImplementedError("publish method is not implemented!")

    @abstractmethod
    def create_topics(self, topics: List[str]) -> None:
        raise NotImplementedError("create_topics method is not implemented!")


class BrokerInterface(metaclass=ABCMeta):
    def __init__(self, succeeding=None):
        self._succeeding = succeeding

    @abstractmethod
    def handle(self) -> None:
        raise NotImplementedError("handle method is not implemented!")


class ServiceInterface(metaclass=ABCMeta):
    @abstractmethod
    def execute(self) -> bool:
        raise NotImplementedError("execute method is not implemented!")
