# Standard library imports
import os
from importlib import reload

# Third party imports
from asynctest import TestCase, mock

# Local application imports
from brandenburg import config


class ConfigTest(TestCase):
    async def test_debug_is_true(self):
        with mock.patch.dict(os.environ, DEBUG="1"):
            s = config.Settings()
            self.assertEqual(s.DEBUG, True)

    async def test_loglevel(self):
        with mock.patch.dict(os.environ, NAMESPACE="PROD", LOG_LEVEL="info"):
            reload(config)
            s = config.Settings()
            self.assertEqual(s.LOG_LEVEL, "info")
