# Third party imports
import aioredis
import pytest
from aioredis.errors import ReplyError

# Local application imports
from brandenburg.config import settings
from brandenburg.services.lead import LeadService


@pytest.fixture
@pytest.mark.asyncio
async def redis(request):
    redis = await aioredis.create_redis_pool(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        db=settings.REDIS_DATABASE,
    )

    async def teardown():  # pragma: no cover
        redis.close()
        await redis.wait_closed()

    request.addfinalizer(teardown)
    return redis
