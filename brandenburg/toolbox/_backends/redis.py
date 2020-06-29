import asyncio
from typing import Tuple, Optional

import aioredis
from aioredis.errors import ReplyError

from brandenburg.toolbox.logger import log

from .base import BaseBackend

logger = log.get_logger(__name__)


class RedisBackend:
    __instance = None

    def __new__(cls, url):
        if RedisBackend.__instance is None:
            RedisBackend.__instance = object.__new__(cls)
        RedisBackend.__instance.url = url
        RedisBackend.__instance.conn = None
        return RedisBackend.__instance

    @staticmethod
    async def get_instance() -> aioredis.commands.Redis:
        """
        Returns a lazily-cached redis conn for the instance's.
        """
        _conn = RedisBackend.__instance.conn
        if _conn is None:
            _conn = await RedisBackend.__instance._get_new_conn()
            RedisBackend.__instance.conn = _conn
        return RedisBackend.__instance

    @classmethod
    async def _get_new_conn(cls) -> None:
        loop = asyncio.get_event_loop()
        return await aioredis.create_redis(cls.__instance.url, loop=loop)

    @classmethod
    async def set_cache(cls, key: str, value: str = "x", ttl: int = 3600) -> bool:
        try:
            await cls.__instance.conn.set(key, value)
            await cls.__instance.conn.expire(key, ttl)
            logger.info(f"Configuring cache for key: {key}")
            return True
        except ReplyError as ex:
            logger.error(ex)
        return False

    @classmethod
    async def is_valid_token(cls, token: str) -> bool:
        try:
            exists: str = await cls.__instance.conn.exists(token)
            if exists:
                return True
        except ReplyError as ex:
            logger.error(ex)

        return False

    async def get_or_create(self, key: str, value: str = "") -> Tuple[str, bool]:
        """
            This avoid the same key to be send twice to be processed
        """
        value: bytes = await self.__instance.conn.get(key) or b"0"
        if int(value) == 1:
            return key, False
        else:
            await self._conn.set(key, value)
            return key, True
        return key, False

    async def get(self, key: str) -> str:
        value: bytes = await self.__instance.conn.get(key)
        if value:
            return value.decode()
        return ""
