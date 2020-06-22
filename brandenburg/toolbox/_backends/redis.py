import asyncio
from typing import Tuple

import aioredis
from aioredis.errors import ReplyError

from brandenburg.toolbox.logger import log

from .base import BaseBackend

logger = log.get_logger(__name__)


class RedisBackend(BaseBackend):
    def __init__(self, url: str):
        self.conn_url = url

    async def connect(self) -> None:
        loop = asyncio.get_event_loop()
        self._conn = await aioredis.create_redis(self.conn_url, loop=loop)

    async def disconnect(self) -> None:
        self._conn.close()

    async def set_cache(self, key: str, value: str = "x", ttl: int = 3600) -> bool:
        try:
            await self._conn.set(key, value)
            await self._conn.expire(key, ttl)
            logger.info(f"Key: {key}, Value: {value} ")
            return True
        except ReplyError as ex:
            logger.error(ex)
        return False

    async def is_valid_token(self, token: str) -> bool:
        try:
            exists: str = await self._conn.exists(token)
            if exists:
                return True
        except ReplyError as ex:
            logger.error(ex)

        return False

    async def get_or_create(self, key: str, value: str = "") -> Tuple[str, bool]:
        """
            This avoid the same key to be send twice to be processed
        """
        value: bytes = await self._conn.get(key) or b"0"
        if int(value) == 1:
            return key, False
        else:
            await self._conn.set(key, value)
            return key, True
        return key, False
