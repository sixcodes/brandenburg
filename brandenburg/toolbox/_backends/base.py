from abc import abstractmethod, ABCMeta


class BaseBackend(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, url):
        raise NotImplementedError("__init__ method is not implemented!")

    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError("connect methos is not implemented!")

    @abstractmethod
    async def disconnect(self) -> None:
        raise NotImplementedError("disconnect method is not implemented!")
