# Standard library imports
import asyncio

# Third party imports
import pytest
from fastapi.testclient import TestClient

# Local application imports
from brandenburg.main import app


@pytest.fixture
def client():
    return TestClient(app)
