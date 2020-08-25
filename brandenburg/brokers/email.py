from brandenburg.config import settings
from brandenburg.interfaces import BrokerInterface
from brandenburg.toolbox.logger import log

LOGGER = log.get_logger(__name__)


class EmailBroker(BrokerInterface):
    pass
