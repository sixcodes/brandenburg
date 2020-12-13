# Standard library imports
from datetime import datetime
from io import StringIO
from typing import Tuple

# Local application imports
from brandenburg.models.batch import BatchModel
from brandenburg.services.publisher import PublisherService
from brandenburg.toolbox.logger import log

logger = log.get_logger(__name__)


class BatchService:
    @staticmethod
    async def execute(batch: BatchModel, routing_key: str, action: str = "upsert") -> Tuple[BatchModel, bool]:
        batch.action = action
        res = await PublisherService.publish(batch.dict(), routing_key)
        logger.info(f"sent_to_topic: {bool(res)}, batch: {batch}")
        return batch, True

    @staticmethod
    async def upload(name: str, filename: str, file: bytes, hash: str, token: str):

        path: str = f"{name}/{datetime.now().strftime('%Y/%m/%d')}"
        logger.info(f"uploading file: {filename} with hash: {hash} to path {path}, token: {token}")
        await PublisherService.upload_file(f"{path}/{filename}", file)
        logger.info("uploading MD5SUM file")
        await PublisherService.upload_file(f"{path}/MD5SUM", StringIO(hash))
        logger.info("all files were uploaded")
        return True
