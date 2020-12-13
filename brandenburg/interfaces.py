# Standard library imports
from abc import abstractmethod, ABCMeta
from typing import List, Dict


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

    @abstractmethod
    def upload_file(self, path: str, file: bytes, **kwargs) -> None:
        raise NotImplementedError("publish method is not implemented!")


class ServiceInterface(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, data: Dict[str, str], context) -> bool:
        raise NotImplementedError("execute method is not implemented!")
