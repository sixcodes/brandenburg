# Standard library imports
import os
from typing import List, Tuple, Dict

# Third party imports
from pydantic import BaseSettings, RedisDsn, Json


class Settings(BaseSettings):
    """
    https://pydantic-docs.helpmanual.io/#settings
    """

    DEBUG: bool = True
    PORT: str = "8000"
    LOG_LEVEL: str = "trace"  # [critical|error|warning|info|debug|trace]
    PROD: bool = False
    NAMESPACE: str = "dev"
    HOST_BIND: str = "127.0.0.1"

    AUTH_USERS: Dict[str, str] = {"ADMIN": "xyz"}
    BATCH_LIMIT: int = 1000

    ALLOWED_HOSTS: List[str] = ["*"]

    REDIS_URL: RedisDsn
    REDIS_POOL_MIN_SIZE: int = 1
    REDIS_POOL_MAX_SIZE: int = 20

    DEFAULT_LOCALE: str = "pt-BR"
    PROVIDER: str = "gcp"  # Option: aws or gcp
    TOPICS: List[str] = [
        "email",
        "sms",
        "whatsapp",
        "salesforce",
        "test_brandenburg",
    ]
    BUCKET_STAGE: str = ""
    TEMPLATE_BUCKET: str = ""

    # GOOGLE
    GOOGLE_PROJECT_ID: str = ""
    GOOGLE_CREDENTIALS: Json

    # AWS
    AWS_SERVER_PUBLIC_KEY: str = ""
    AWS_SERVER_SECRET_KEY: str = ""
    AWS_REGION: str = "us-east-1"

    class Config:
        env_file = "dev.env"
        env_file_encoding = "utf-8"


settings = Settings()
