from abc import abstractmethod, ABCMeta


class BaseBackend(metaclass=ABCMeta):
    @abstractmethod
    def __new__(self, url):
        raise NotImplementedError("__init__ method is not implemented!")

    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError("connect methos is not implemented!")

    @abstractmethod
    async def disconnect(self) -> None:
        raise NotImplementedError("disconnect method is not implemented!")


class BaseBackendMeta(type):
    def __init__(cls, name, bases, dict):
        super(BaseBackendMeta, cls).__init__(name, bases, dict)
        original_new = cls.__new__

        def _new(cls, *args, **kwds):
            if cls.instance is None:
                cls.instance = original_new(cls, *args, **kwds)
            return cls.instance

        cls.instance = None
        cls.__new__ = staticmethod(_new)
