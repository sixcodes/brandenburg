from typing import List, Tuple, Dict, Union

from brandenburg.brokers.salesforce import SalesforceBroker
from brandenburg.config import settings
from brandenburg.interfaces import ServiceInterface
from brandenburg.toolbox.funcs import Funcs
from brandenburg.toolbox.logger import log

logger = log.get_logger(__name__)


class MarketingService(ServiceInterface):
    @staticmethod
    def execute(event: Dict[str, str], context):
        logger.info("Starting service")
        data: Dict[str, str] = Funcs.decode(event.get("data"))
        attrs: Dict[str, str] = event.get("attributes")
        sf: SalesforceBroker = SalesforceBroker()
        sf.handle(data)
