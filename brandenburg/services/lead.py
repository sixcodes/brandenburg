import asyncio
import json
import pickle
import uuid
from typing import List, Tuple, Dict, Union

from pydantic import ValidationError

from brandenburg.config import settings
from brandenburg.models.lead import LeadModel
from brandenburg.services.publisher import PublisherService
from brandenburg.toolbox._backends.redis import RedisBackend
from brandenburg.toolbox.logger import log

logger = log.get_logger(__name__)


class LeadService:
    @staticmethod
    async def execute(token: str, lead: LeadModel) -> Union[bool, Tuple[Dict[str, Union[str, List[str]]], bool]]:
        cache = await RedisBackend(settings.REDIS_URL).get_instance()

        is_valid: bool = await cache.is_valid_token(token)
        if is_valid:
            logger.info(f"Is valid token with data")
            res = await PublisherService.publish(lead.dict(), lead.by)
            logger.info(f"sent_to_queue: {bool(res)}, lead: {lead}")
            return lead.dict(), True
        return {"status": "error", "message": f"Token {token} is invalid"}, False
