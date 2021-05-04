# Standard library imports
from typing import List

# Local application imports
from brandenburg.providers.aws import AWS
from brandenburg.providers.gcp import GCP
from brandenburg.toolbox.logger import logger


class ProviderStrategy:
    def __init__(self, strategy: str) -> None:
        self._strategy = self.__factory(strategy)()

    def __factory(self, strategy):
        try:
            return {"gcp": GCP, "aws": AWS}.get(strategy.lower(), None)
        except AttributeError as ex:
            logger.error(ex)

    def context_publish(self, topic: str, data: bytes, **attrs):
        self._strategy.publish(topic, data, **attrs)

    def context_create_topics(self, topics: List[str]):
        self._strategy.create_topics(topics)

    def context_upload_file(self, path: str, file: bytes, **kwargs):
        self._strategy.upload_file(path, file, **kwargs)
