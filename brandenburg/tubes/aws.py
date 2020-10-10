from typing import Dict

from brandenburg.config import settings
from brandenburg.interfaces import TubeInterface
from brandenburg.toolbox.logger import log
from brandenburg.toolbox.smtpx import SMTPX

LOGGER = log.get_logger(__name__)


class AWSMailTube(TubeInterface):
    def handle(self, data: Dict[str, str]):
        mail = SMTPX(user=settings.AWS_SMTP_USER, password=settings.AWS_SMTP_PASSWORD, host=settings.AWS_SMTP_HOST)
        mail.send()


class AWSSMSTube(TubeInterface):
    def handle(self, data: Dict[str, str]):
        pass
