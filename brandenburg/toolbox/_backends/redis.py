# Standard library imports
import asyncio
from typing import Tuple, Optional

# Third party imports
import aioredis
from aioredis.errors import ReplyError, ConnectionForcedCloseError
from pydantic import RedisDsn

# Local application imports
from brandenburg.config import settings
from brandenburg.toolbox.logger import logger


class RedisBackend:
    def __init__(self, url: RedisDsn):
        self.url = url
        self.is_connected = False
        self._pool = None

    async def connect(self) -> None:
        assert self._pool is None, "RedisBackend is already running"
        loop = asyncio.get_event_loop()
        await logger.info("Initializing redis connection pool...")
        self._pool = await aioredis.create_redis_pool(
            self.url,
            minsize=settings.REDIS_POOL_MIN_SIZE,
            maxsize=settings.REDIS_POOL_MAX_SIZE,
            loop=loop,
        )
        self.is_connected = True

    async def disconnect(self) -> None:
        """
        aioredis.commands.ContextRedis
        """
        assert self._pool is not None, "RedisBackend is not running"
        try:
            self._pool.close()
            await logger.info("Closing redis connection")
            await self._pool.wait_closed()
            self.is_connected = False
        except ConnectionForcedCloseError as ex:
            await logger.error(ex)

    async def __aenter__(self) -> "RedisBackend":
        await self.connect()
        return self

    async def __aexit__(self, **kwargs) -> None:
        await self.disconnect()

    async def get(self, key: str) -> str:
        """
        ...
        """
        try:
            data: bytes = await self._pool.get(key)
            return data.decode()
        except ReplyError as ex:
            await logger.error(ex)
        return False

    async def set(self, key: str, value: str) -> Optional[bool]:
        """
        ....
        """
        try:
            await logger.info(f"Configuring cache for key: {key}")
            await self._pool.set(key, value)
            return True
        except ReplyError as ex:
            await logger.error(ex)
        return False

    async def set_ex(self, key: str, value: str, ttl: int = 600) -> Optional[bool]:
        """
        ....
        """
        try:
            await logger.info(f"Configuring cache for key: {key}")
            await self._pool.set(key, value)
            await self._pool.expire(key, ttl)
            return True
        except ReplyError as ex:
            await logger.error(ex)
        return False

    async def exists(self, token: str) -> Optional[bool]:
        try:
            exists: str = await self._pool.exists(token)
            await logger.info("Disconnecting from redis cluster")
            if exists:
                return True
        except ReplyError as ex:
            await logger.error(ex)

        return False

    async def is_valid_token(self, token: str) -> Optional[bool]:
        try:
            exists: str = await self._pool.exists(token)
            if exists:
                return True
        except ReplyError as ex:
            await logger.error(ex)

        return False

    async def get_or_create(self, key: str, value: str = "") -> Tuple[str, bool]:
        """
        This avoid the same key to be send twice to be processed
        """
        value: bytes = await self._pool.get(key) or b"0"
        if int(value) == 1:
            return key, False
        else:
            await self._pool.set(key, value)
            return key, True
        return key, False

    async def set_table_last_updated(self, table: str, updated_at: int) -> None:
        """
        ...
        """
        last_updated_ts: int = max(int(await self._pool.get(key=table) or 0), updated_at)
        await logger.info(f"Configuring last ran date to table: {table}, timestamp: {last_updated_ts}")
        await cls.set(key=table, value=last_updated_ts)
        await logger.info("last ran was set successfully")
