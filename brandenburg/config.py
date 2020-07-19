import os
from typing import List, Tuple

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

    AUTH_USERS: List[List[str]]
    BATCH_LIMIT: int = 1000

    ALLOWED_HOSTS: List[str] = ["*"]
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_POOL_MIN_SIZE: int = 1
    REDIS_POOL_MAX_SIZE: int = 20

    DEFAULT_LOCALE: str = "pt-BR"
    PROVIDER: str = "gcp"  # Option: aws or gcp
    TOPICS: List[str] = ["email", "sms", "whatsapp", "salesforce"]
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
    SENDGRID_USERNAME: str = ""
    SENDGRID_PASSWORD: str = ""

    # Mailgun
    MAILGUN_USERNAME: str = ""
    MAILGUN_PASSWORD: str = ""

    # GOOGLE
    GOOGLE_PROJECT_ID: str
    GOOGLE_CREDENTIALS: Json
    GOOGLE_TEMPLATE_BUCKET: str

    # AWS
    AWS_SERVER_PUBLIC_KEY: str = ""
    AWS_SERVER_SECRET_KEY: str = ""
    AWS_REGION: str = "us-east-1"

    class Config:
        env_file = 'dev.env'
        env_file_encoding = 'utf-8'

settings = Settings()
