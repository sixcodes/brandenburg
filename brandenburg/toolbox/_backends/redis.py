import asyncio
from typing import Tuple

import aioredis
from aioredis.errors import ReplyError

from brandenburg.config import settings
from brandenburg.toolbox.logger import log

logger = log.get_logger(__name__)


class RedisBackend:
    __instance: aioredis.Redis = None

    def __new__(cls, url: str):
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
        return await aioredis.create_redis_pool(
            cls.__instance.url, minsize=settings.REDIS_POOL_MIN_SIZE, maxsize=settings.REDIS_POOL_MAX_SIZE, loop=loop
        )

    @classmethod
    async def disconnect(cls) -> None:
        with await cls.__instance.conn as cache:
            await cache.clear()
            await cache.wait_close()

    @classmethod
    async def set_cache(cls, key: str, value: str = "x", ttl: int = 3600) -> bool:
        try:
            with await cls.__instance.conn as cache:
                await cache.set(key, value)
                await cache.expire(key, ttl)
            logger.info(f"Configuring cache for key: {key}")
            return True
        except ReplyError as ex:
            logger.error(ex)
        return False

    @classmethod
    async def is_valid_token(cls, token: str) -> bool:
        try:
            with await cls.__instance.conn as cache:
                exists: str = await cache.exists(token)
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

    @classmethod
    async def get(cls, key: str) -> str:

        with await cls.__instance.conn as cache:
            value: bytes = await cache.get(key)
        if value:
            return value.decode()
        return ""
