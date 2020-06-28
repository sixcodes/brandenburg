import base64
import re
import string
from typing import List, Union, Dict, Tuple

import boto3
from structlog import get_logger

from brokers.aws import AWSBroker
from config import settings
# TODO: move to a good place
from providers.gcp import GCP

logger = get_logger(__name__)


class EmailService:
    @staticmethod
    def run():
        gcs = storage.Client(project=settings.GOOGLE_PROJECT_ID, credentials=GCP().get_credentials())
        kind, locale, template_name = "email", "pt_BR", "verification_code"
        template: str = f"{kind}/{locale}/{template_name}.html"

        file = gcs.get_bucket(settings.GOOGLE_TEMPLATE_BUCKET).get_blob(template).download_as_string()
        file.format()

        aws = AWSBroker()
        # mandrill = MandrillBroker(aws)
        # sendgrid = SendgridBroker(mandrill)
        aws.handle(subject, sender, to_address, body)
