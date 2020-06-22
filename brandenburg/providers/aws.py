from typing import List

from brandenburg.config import settings
from brandenburg.interfaces import ProviderInterface


class AWS(ProviderInterface):
    """
    Services to be used such as SQS and Kinesis
    """

    def get_credentials(self):
        raise NotImplementedError("get_credentials method is not implemented!")

    def publish(self, topic: str, data, **kwargs):
        raise NotImplementedError("publish method is not implemented!")

    def create_topics(self, topics: List[str]):
        raise NotImplementedError("create_topics method is not implemented!")
