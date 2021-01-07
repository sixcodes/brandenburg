# Standard library imports
from datetime import datetime
from io import StringIO
from typing import Tuple

# Local application imports
from brandenburg.config import settings
from brandenburg.models.batch import BatchModel
from brandenburg.services.publisher import PublisherService
from brandenburg.toolbox._backends.redis import RedisBackend
from brandenburg.toolbox.logger import log

LOGGER = log.get_logger(__name__)


class BatchService:
    @classmethod
    async def execute(cls, batch: BatchModel, routing_key: str, action: str = "upsert") -> Tuple[BatchModel, bool]:
        batch.action = action
        res = await PublisherService.publish(batch.dict(), routing_key)
        LOGGER.info(f"sent_to_topic: {bool(res)}, batch: {batch}")
        cls._set_last_ran(batch)
        return batch, True

    @staticmethod
    async def upload(name: str, filename: str, file: bytes, hash: str, token: str) -> bool:

        path: str = f"{name}/{datetime.now().strftime('%Y/%m/%d')}"
        LOGGER.info(f"uploading file: {filename} with hash: {hash} to path {path}, token: {token}")
        await PublisherService.upload_file(f"{path}/{filename}", file)
        LOGGER.info("uploading MD5SUM file")
        await PublisherService.upload_file(f"{path}/MD5SUM", StringIO(hash))
        LOGGER.info("all files were uploaded")
        return True

    @classmethod
    async def _set_last_ran(cls, batch: BatchModel) -> None:
        cache = await RedisBackend(settings.REDIS_URL).get_instance()
        LOGGER.info(f"Configuring last ran date to table: {batch.table_name}, timestamp: {batch.last_updated_at}")
        cache.set_cache(batch.table_name.lower(), batch.last_updated_at, -1)
        LOGGER.info("last ran was set successfully")
