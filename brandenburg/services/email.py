from typing import List, Union, Dict, Tuple

from brandenburg.models.notify import NotifyModel
from brandenburg.toolbox.logger import log
from brokers.aws import AWSBroker
from config import settings
from providers.gcp import GCP

logger = log.get_logger(__name__)


class EmailService:
    @staticmethod
    def execute(notify: NotifyModel):
        gcs = storage.Client(project=settings.GOOGLE_PROJECT_ID, credentials=GCP().get_credentials())
        kind, locale, template_name = "email", "pt_BR", "verification_code"
        template: str = f"{kind}/{locale}/{template_name}.html"

        file = gcs.get_bucket(settings.GOOGLE_TEMPLATE_BUCKET).get_blob(template).download_as_string()
        file.format()

        aws = AWSBroker()
        # mandrill = MandrillBroker(aws)
        # sendgrid = SendgridBroker(mandrill)
        aws.handle(subject, sender, to_address, body)
