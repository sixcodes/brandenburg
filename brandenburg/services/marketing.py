from typing import Dict, Union

from google.cloud.functions.context import Context

from brandenburg.brokers.salesforce import SalesforceTube
from brandenburg.interfaces import ServiceInterface
from brandenburg.toolbox.funcs import Funcs
from brandenburg.toolbox.logger import log

LOGGER = log.get_logger(__name__)


class MarketingService(ServiceInterface):
    @staticmethod
    def execute(event: Dict[str, str], context: Context) -> bool:
        """
        TODO: rethink COntext direct from google when aws ?
        """
        LOGGER.info("Starting service")
        data: Dict[str, str] = Funcs.decode(event.get("data", ""))
        LOGGER.info(f"Data received: {data} ")
        attrs: Union[Dict[str, str], str] = event.get("attributes", {})
        LOGGER.info(f"Attributes: {attrs}")
        sf: SalesforceTube = SalesforceTube()
        processed: bool = sf.handle(data)

        return processed
