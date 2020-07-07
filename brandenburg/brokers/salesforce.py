from typing import Dict

import ET_Client
from structlog import get_logger

from brandenburg.config import settings
from brandenburg.interfaces import BrokerInterface

logger = get_logger(__name__)


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

    def create_data_extension(self, table_name: str, customer_key: str, message: List[Dict[str, str]]):
        """
         [{"Name" : "Name", "FieldType" : "Text",  "MaxLength" : "255"},
         {"Name" : "phone_number", "FieldType" : "Text",  "MaxLength" : "13"},
         {"Name" : "email", "FieldType" : "EmailAddress", "IsPrimaryKey" : "true", "IsRequired" : "true"}]
        """
        logger.info(f'Creating new {table_name} Data Extension')
        data_extension = ET_Client.ET_DataExtension()
        data_extension.auth_stub = self.get_client()

        data_extension.props = {"Name": table_name, "CustomerKey": customer_key}
        data_extension.columns = message
        response = data_extension.post()
        logger.info(f"post_tatus: {str(response.status)}, code: {str(response.code)}, message: {str(response.message)}")
        logger.info("Results: " + str(response.results))
        if int(response.status) == 200:  # HTTPStatus.OK
            return True
        return False

    def send_new_row(self, message: Dict[str, str], extension_key: str) -> bool:
        """
        :param message: the list of dict wiht the data
        :param extension_key: it is the customer key or 'table name'
        """
        logger.info("Adding a row to a data extension")
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

    def update_row(self, message: Dict[str, str], extension_key: str) -> bool:
        """
        :param message: the list of dict wiht the data
        :param extension_key: it is the customer key or 'table name'
        """
        logger.info("Adding a row to a data extension")
        row = ET_Client.ET_DataExtension_Row()
        row.CustomerKey = extension_key
        row.auth_stub = self.get_client()
        row.props = message
        response = row.patch()
        logger.info(
            f"patch_tatus: {str(response.status)}, code: {str(response.code)}, message: {str(response.message)}"
        )
        logger.info("Results: " + str(response.results))
        if int(response.status) == 200:
            return True
        return False

    def handle(self, data: Dict[str, str]) -> bool:
        """
        TODO: Check to where it must be sent and call the right function
        """
        logger.info("handling")

        self.send_new_row(data)
