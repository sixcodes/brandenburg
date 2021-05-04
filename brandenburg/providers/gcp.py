# Standard library imports
from functools import lru_cache
from typing import Tuple, List

# Third party imports
from google.cloud import pubsub_v1, storage
from google.oauth2.service_account import Credentials
from pydantic.types import Json

# Local application imports
from brandenburg.config import settings
from brandenburg.interfaces import ProviderInterface
from brandenburg.toolbox.logger import logger


def pub_client():
    # Configure the retry settings. Defaults will be overwritten.
    google_credentials: Json = settings.GOOGLE_CREDENTIALS
    if google_credentials:
        credentials = Credentials.from_service_account_info(google_credentials)
    else:
        credentials = Credentials()

    retry_settings = {
        "interfaces": {
            "google.pubsub.v1.Publisher": {
                "retry_codes": {
                    "publish": [
                        "ABORTED",
                        "CANCELLED",
                        "DEADLINE_EXCEEDED",
                        "INTERNAL",
                        "RESOURCE_EXHAUSTED",
                        "UNAVAILABLE",
                        "UNKNOWN",
                    ]
                },
                "retry_params": {
                    "messaging": {
                        "initial_retry_delay_millis": 100,  # default: 100
                        "retry_delay_multiplier": 1.3,  # default: 1.3
                        "max_retry_delay_millis": 60000,  # default: 60000
                        "initial_rpc_timeout_millis": 5000,  # default: 25000
                        "rpc_timeout_multiplier": 1.0,  # default: 1.0
                        "max_rpc_timeout_millis": 600000,  # default: 30000
                        "total_timeout_millis": 600000,  # default: 600000
                    }
                },
                "methods": {
                    "Publish": {
                        "retry_codes_name": "publish",
                        "retry_params_name": "messaging",
                    }
                },
            }
        }
    }
    logger.debug("<<<<<<<<<< create a connection >>>>>>>>>")
    return pubsub_v1.PublisherClient(credentials=credentials)


publisher_client = pub_client()


class GCP(ProviderInterface):
    @lru_cache(512)
    def get_credentials(self):
        """
        TODO: checkif credentials exist if not try to auth with local credentials
        """
        scopes: Tuple[str, str, str] = (
            "https://www.googleapis.com/auth/bigquery",
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/drive",
        )
        credentials: Credentials
        google_credentials: Json = settings.GOOGLE_CREDENTIALS
        if google_credentials:
            credentials = Credentials.from_service_account_info(google_credentials)
        else:
            credentials = Credentials()
        logger.info("Authenticating on GCP")
        credentials = credentials.with_scopes(scopes)
        return credentials

    def create_topics(self, topics: List[str]) -> None:
        """
        TODO: Add a return statement and handle with exceptions
        """
        GOOGLE_PROJECT_ID: str = settings.GOOGLE_PROJECT_ID
        client: pubsub_v1.PublisherClient = publisher_client
        logger.info(f"Checking if all topics already exists")
        existing_topics: List[str] = [
            element.name.split("/")[3] for element in client.list_topics(project=f"projects/{GOOGLE_PROJECT_ID}")
        ]
        logger.info(f"Existing opics: { existing_topics}")
        for topic in set(topics).difference(existing_topics):
            topic_name: str = client.topic_path(GOOGLE_PROJECT_ID, topic)
            logger.info(f"creating topic: {topic_name}")
            try:
                client.create_topic(topic_name)
            except Exception as ex:
                logger.error(ex)

    def publish(self, topic: str, data: str, **attrs):
        """
        TODO: handle exceptions and retries
        Future: https://github.com/googleapis/python-api-core/blob/02d25799243bd76ac76423a08c063a2bee8d11e4/google/api_core/future/base.py#L23
        """

        topic_name: str = f"projects/{settings.GOOGLE_PROJECT_ID}/topics/{topic}"
        future = publisher_client.publish(topic_name, data, **attrs)
        logger.info(f"Futures: {future.result()}")

    def upload_file(self, path: str, file: bytes, **kwargs):
        """
        TODO: add exception cases and return statement
        """
        bucket = storage.Client(
            project=settings.GOOGLE_PROJECT_ID,
            credentials=self.get_credentials(),
        ).get_bucket(settings.BUCKET_STAGE)

        blob = storage.Blob(path, bucket).upload_from_file(file)
