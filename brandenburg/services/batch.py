# Standard library imports
from datetime import datetime
from io import StringIO
from typing import Tuple

# Local application imports
from brandenburg import cache
from brandenburg.models.batch import BatchModel
from brandenburg.services.publisher import PublisherService
from brandenburg.toolbox.logger import logger


class BatchService:
    @classmethod
    async def execute(cls, batch: BatchModel, routing_key: str, action: str = "upsert") -> Tuple[BatchModel, bool]:
        batch.action = action
        res = await PublisherService.publish(batch.dict(), routing_key)
        await logger.info(f"sent_to_topic: {bool(res)}, batch: {batch}")
        await cls._set_last_ran(batch)
        return batch, True

    @staticmethod
    async def upload(name: str, filename: str, file: bytes, hash: str, token: str) -> bool:

        path: str = f"{name}/{datetime.now().strftime('%Y/%m/%d')}"
        await logger.info(f"uploading file: {filename} with hash: {hash} to path {path}, token: {token}")
        await PublisherService.upload_file(f"{path}/{filename}", file)
        await logger.info("uploading MD5SUM file")
        await PublisherService.upload_file(f"{path}/MD5SUM", StringIO(hash))
        await logger.info("all files were uploaded")
        return True

    @classmethod
    async def _set_last_ran(cls, batch: BatchModel) -> None:

        table: str = batch.table_name.lower()
        updated_at: int = batch.last_updated_at
        await cache.set_table_last_updated(table, updated_at)
