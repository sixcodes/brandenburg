__version__ = "0.5.0"
# Local application imports
from brandenburg.config import settings
from brandenburg.toolbox._backends.redis import RedisBackend

cache: RedisBackend = RedisBackend(settings.REDIS_URL)
