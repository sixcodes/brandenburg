# Standard library imports
import base64
import re
import uuid
from typing import Union, Dict, Tuple

# Third party imports
import orjson as json

# Local application imports
from brandenburg.config import settings
from brandenburg.toolbox._backends.redis import RedisBackend
from brandenburg.toolbox.logger import logger


class Funcs:
    # @staticmethod
    # def encode_image(path: str) -> bytes:
    #     with open(path, "rb") as image:
    #         encoded = base64.b64encode(image.read())
    #     return encoded

    @staticmethod
    async def _generate_token() -> str:
        """
        Generate a UUID just to track the user request
        """
        return str(uuid.uuid4())

    @classmethod
    async def generate_token(cls, value: str = "") -> str:
        redis = await RedisBackend(settings.REDIS_URL).get_instance()
        token: str = await cls._generate_token()
        ok: bool = await redis.set_cache(token, value)
        if not ok:
            await redis.set_cache(redis, token, value)
        return token

    @staticmethod
    def encode(data: Union[Dict[str, str], str, int]) -> str:
        """
        param: data
        Can be a string, a dict or a integer and the function will return a encoded string
        """
        if isinstance(data, dict):
            return base64.b64encode(json.dumps(data).encode()).decode()
        else:
            return base64.b64encode(str(data).encode()).decode()

    @staticmethod
    def decode(data: str) -> Union[Dict[str, str], int, str]:
        try:
            decoded = json.loads(base64.b64decode(data).decode())
            if isinstance(decoded, dict):
                return decoded
        except ValueError as ex:
            logger.error(f"An error ocurred trying decode {data}, error: {ex}")
        try:
            return base64.b64decode(data.encode()).decode()
        except ValueError as ex:
            logger.error(f"An error ocurred trying decode {data}, error: {ex}")
            return data

    @staticmethod
    def normalize_phonenumber(number: str) -> str:
        """
        https://saimana.com/list-of-country-locale-code/
        https://pypi.org/project/phonenumbers/
        """
        # TODO: Must normalize phone number using locale
        clean_number: str = re.sub("[^\d+]", "", number)
        if len(clean_number) == 11:
            logger.info(f"Number {number[:6]} was normalized")
            return f"+55{clean_number}"
        elif len(clean_number) < 11:
            return ""
        else:
            return f"+{clean_number}"
