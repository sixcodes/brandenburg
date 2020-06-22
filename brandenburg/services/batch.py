import asyncio
from typing import List, Tuple

from pydantic import ValidationError, Json

from brandenburg.models.batch import BatchModel
from brandenburg.services.publisher import PublisherService
from brandenburg.toolbox.logger import log

logger = log.get_logger(__name__)


class BatchService:
    async def execute(batch: BatchModel, routing_key: str, action: str = "upsert") -> Tuple[BatchModel, bool]:
        batch.action = action
        res = await PublisherService.publish(batch.dict(), "import_push")
        logger.info(f"sent_to_topic: {bool(res)}, batch: {batch}")
        return batch, True
