# Standard library imports
from typing import Dict

# Third party imports
from orjson import dumps

# Local application imports
from brandenburg.config import settings
from brandenburg.strategies import ProviderStrategy
from brandenburg.toolbox.logger import logger


class PublisherService:
    @staticmethod
    async def publish(data: Dict[str, str], routing_key: str) -> bool:
        topic: str = f"{routing_key}_{settings.NAMESPACE}"
        await logger.info(f"sending messsage to topic: {topic}")
        published = await ProviderStrategy(settings.PROVIDER).context_publish(topic, dumps(data))
        return published

    @staticmethod
    async def upload_file(path: str, file, **kwargs) -> bool:
        full_path: str = f"{settings.NAMESPACE}/{path}"
        uploaded = await ProviderStrategy(settings.PROVIDER).context_upload_file(full_path, file)
        return uploaded
