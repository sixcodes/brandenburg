# Third party imports

# Standard library imports
import asyncio
import logging

# Third party imports
from aiologger.loggers.json import JsonLogger

logger = JsonLogger.with_default_handlers(level=logging.DEBUG, extra={"applicationName": "araguaia"})
