# Standard library imports
import asyncio  # pragma: nocover
from typing import List, Tuple, Dict, Union

# Local application imports
from brandenburg import cache
from brandenburg.models.lead import LeadModel
from brandenburg.services.publisher import PublisherService
from brandenburg.toolbox.logger import logger


class LeadService:
    @staticmethod
    async def execute(token: str, lead: LeadModel) -> Union[bool, Tuple[Dict[str, Union[str, List[str]]], bool]]:
        """
        TODO:
        """
        #TODO: Improve the return type, to be more especific
        is_valid: bool = await cache.is_valid_token(token)
        if is_valid:
            await logger.info(f"Is valid token with data")
            res = await PublisherService.publish(lead.dict(), lead.by)
            await logger.info(f"sent_to_queue: {bool(res)}, lead: {lead}")
            return lead.dict(), True
        return (
            {"status": "error", "message": f"Token {token} is invalid"},
            False,
        )
