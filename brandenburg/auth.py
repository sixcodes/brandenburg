import secrets
from typing import List

import aioredis

from brandenburg.config import settings
from brandenburg.toolbox._backends.redis import RedisBackend

try:
    from fastapi import status, Depends, HTTPException
    from fastapi.security import HTTPBasic, HTTPBasicCredentials

    security = HTTPBasic()
except ImportError:
    pass


async def get_fast_auth(
    credentials: HTTPBasicCredentials = Depends(security),
    cache: aioredis.Redis = Depends(RedisBackend(settings.REDIS_URL).get_instance),
) -> None:
    """
    By using the secrets.compare_digest() it will be secure against a type of attacks called "timing attacks".
    """
    username: str = credentials.username.upper()
    password: str = await cache.get(username)
    correct_username = secrets.compare_digest(credentials.username, username)
    correct_password = secrets.compare_digest(credentials.password, password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect auth token",
            headers={"WWW-Authenticate": "Basic"},
        )


async def create_users(auth_users: List[List[str]] = None) -> None:
    """
    Create users on cache to be used on auth system

    """
    TTL: int = 525600  # One year #TODO: turn it flexible
    cache = await RedisBackend(settings.REDIS_URL).get_instance()
    for value in settings.AUTH_USERS:
        await cache.set_cache(value[0], value[1], TTL)
