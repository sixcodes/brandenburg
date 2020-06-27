from typing import Dict

from ujson import dumps

from brandenburg.config import settings
from brandenburg.strategies import ProviderStrategy
from brandenburg.toolbox.funcs import Funcs


class PublisherService:
    @staticmethod
    async def publish(data: Dict[str, str], routing_key: str) -> bool:
        topic: str = f"{routing_key}_{settings.NAMESPACE}"
        published = ProviderStrategy(settings.PROVIDER).context_publish(topic, dumps(data).encode())
        return published

    @staticmethod
    async def upload_file(path: str, file, **kwargs) -> bool:
        full_path: str = f"{settings.NAMESPACE}/{path}"
        uploaded = ProviderStrategy(settings.PROVIDER).context_upload_file(full_path, file)
        return uploaded
