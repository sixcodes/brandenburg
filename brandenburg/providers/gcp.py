import json
from typing import Tuple, List, Dict

from google.cloud import pubsub_v1
from google.cloud.bigquery import Client
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from pydantic.types import Json
from structlog import get_logger

from brandenburg.config import settings
from brandenburg.interfaces import ProviderInterface

logger = get_logger(__name__)


class GCP(ProviderInterface):
    def get_credentials(self):
        """
        TODO: checkif credentials exist if not try to auth with local credentials
        """
        scopes: Tuple[str] = (
            "https://www.googleapis.com/auth/bigquery",
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/drive",
        )
        google_credentials: Dict[str, str] = json.loads(settings.GOOGLE_CREDENTIALS)
        logger.info("Authenticating on GCP")
        credentials = Credentials.from_service_account_info(google_credentials)
        credentials = credentials.with_scopes(scopes)
        return credentials

    def create_topics(self, topics: List[str]) -> None:
        """
            TODO: Add a return statement and handle with exceptions
        """
        GOOGLE_PROJECT_ID: str = settings.GOOGLE_PROJECT_ID
        client: PublisherClient = pubsub_v1.PublisherClient(credentials=self.get_credentials())
        project = client.project_path(GOOGLE_PROJECT_ID)
        logger.info(f"Checking if all topics already exists")
        existing_topics: List[str] = [element.name.split("/")[3] for element in client.list_topics(project)]
        logger.info(f"Existing opics: { existing_topics}")
        for topic in set(topics).difference(existing_topics):
            topic_name: str = client.topic_path(GOOGLE_PROJECT_ID, topic)
            logger.info(f"creating topic: {topic_name}")
            client.create_topic(topic_name)

    def publish(self, topic: str, data: str, **attrs):
        """
            TODO: handle exceptions and retries
            Future: https://github.com/googleapis/python-api-core/blob/02d25799243bd76ac76423a08c063a2bee8d11e4/google/api_core/future/base.py#L23
        """
        # Configure the retry settings. Defaults will be overwritten.
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
                    "methods": {"Publish": {"retry_codes_name": "publish", "retry_params_name": "messaging"}},
                }
            }
        }

        topic_name: str = f"projects/{settings.GOOGLE_PROJECT_ID}/topics/{topic}"
        client = pubsub_v1.PublisherClient(client_config=retry_settings, credentials=self.get_credentials())
        future = client.publish(topic_name, data, **attrs)
        logger.info(f"Futures: {future.result()}")
