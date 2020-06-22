import asyncio

import pytest

from brandenburg.main import app

from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(app)
