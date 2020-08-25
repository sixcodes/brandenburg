from typing import Dict

from google.cloud.functions.context import Context

from brandenburg.brokers.salesforce import SalesforceBroker
from brandenburg.interfaces import ServiceInterface
from brandenburg.toolbox.funcs import Funcs
from brandenburg.toolbox.logger import log

logger = log.get_logger(__name__)


class MarketingService(ServiceInterface):
    @staticmethod
    def execute(event: Dict[str, str], context: Context):
        logger.info("Starting service")
        data: Dict[str, str] = Funcs.decode(event.get("data"))
        logger.info(f"Data received to send to SF: {data} ")
        attrs: Dict[str, str] = event.get("attributes")
        logger.info(f"Attributes: {attrs}")
        sf: SalesforceBroker = SalesforceBroker()
        sf.handle(data)
