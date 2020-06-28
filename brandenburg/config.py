import os
from functools import lru_cache
from typing import List, Tuple

from pydantic import BaseSettings, RedisDsn, Json


class Settings(BaseSettings):
    """
        https://pydantic-docs.helpmanual.io/#settings
    """

    DEBUG: bool = True
    PORT: str = "8000"
    ACCESS_LOG: bool = False
    PROD: bool = False
    NAMESPACE: str = "dev"

    AUTH_USERS: List[List[str]] = [["ADMIN", "xyz"]]

    ALLOWED_HOSTS: List[str] = ["*"]
    REDIS_URL: str = "redis://localhost:6379"

    DEFAULT_LOCALE: str = "pt-BR"
    PROVIDER: str = "gcp"  # Option: aws or gcp
    TOPICS: List[str] = ["email", "sms", "whatsapp", "salesforce", "sap"]
    BUCKET_STAGE: str = ""

    # SALESFORCE
    SF_CLIENT_ID: str = ""
    SF_ACCOUNT_ID: str = ""
    SF_CLIENT_SECRET: str = ""

    # TWILIO
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_REGION: str = ""
    TWILIO_EDGE: str = ""

    # SENDGRID
    # Mandrill

    # GOOGLE
    GOOGLE_PROJECT_ID: str = ""
    GOOGLE_CREDENTIALS: str = ""  # TODO: CHange this type to Json
    GOOGLE_TEMPLATE_BUCKET: str = ""

    # AWS
    AWS_SERVER_PUBLIC_KEY: str = ""
    AWS_SERVER_SECRET_KEY: str = ""
    AWS_REGION: str = "us-east-1"


@lru_cache(512)
def settings():
    pass


settings = Settings()
