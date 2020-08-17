from typing import List, Tuple, Dict, Union

import ET_Client
import ujson as json

from brandenburg.config import settings
from brandenburg.interfaces import BrokerInterface
from brandenburg.toolbox.logger import log

logger = log.get_logger(__name__)


class SalesforceBroker(BrokerInterface):
    def get_client(self):
        client: ET_Client = ET_Client.ET_Client(
            False,
            False,
            {
                "clientid": settings.SF_CLIENT_ID,
                "clientsecret": settings.SF_CLIENT_SECRET,
                "authenticationurl": f"https://{settings.SF_ACCOUNT_ID}.auth.marketingcloudapis.com/",
                "baseapiurl": f"https://{settings.SF_ACCOUNT_ID}.rest.marketingcloudapis.com/",
                "soapendpoint": f"https://{settings.SF_ACCOUNT_ID}.soap.marketingcloudapis.com/",
                "useOAuth2Authentication": "True",
            },
        )
        return client

    def send_rows(self, message: Dict[str, str], extension_key: str) -> bool:
        """
        :param message: the list of dict wiht the data
        :param extension_key: it is the customer key or 'table name'
        """
        logger.info(f"Adding a row {message} to a data extension")
        row = ET_Client.ET_DataExtension_Row()
        row.CustomerKey = extension_key
        row.auth_stub = self.get_client()
        row.props = message
        response = row.post()
        logger.info(f"post_tatus: {str(response.status)}, code: {str(response.code)}, message: {str(response.message)}")
        logger.info("Results: " + str(response.results))
        if int(response.status) == 200:
            return True
        return False

    def handle(self, data: Dict[str, str]) -> bool:
        """
        TODO: Check to where it must be sent and call the right function
        """
        logger.info("handling")

        self.send_rows(data, settings.SF_LEAD_CUSTOMER_KEY)
