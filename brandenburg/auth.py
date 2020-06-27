import secrets
from typing import List

from brandenburg.config import settings
from brandenburg.toolbox._backends.redis import RedisBackend

try:
    from fastapi import status, Depends, HTTPException
    from fastapi.security import HTTPBasic, HTTPBasicCredentials

    security = HTTPBasic()
except ImportError:
    pass

cache = RedisBackend(settings.REDIS_URL)


async def get_fast_auth(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    """
    By using the secrets.compare_digest() it will be secure against a type of attacks called "timing attacks".
    """

    await cache.connect()
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
    await cache.connect()
    for value in settings.AUTH_USERS:
        await cache.set_cache(value[0], value[1], TTL)
