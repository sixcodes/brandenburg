import asyncio
import json
from typing import Dict

import aioredis
import pytest

from brandenburg.config import settings

NOTIFY = {
    "contact": "jesuesousa@gmail.com",
    "by": "email",
    "template_name": "mail_template",
    "data": {"logo_url": "https://site", "username": "maria", "token": "123456"},
}

# TODO: Move HEADERS to conftest file
HEADERS: Dict[str, str] = {"Origin": "*/*", "Content-Type": "application/json", "Authorization": "Basic QURNSU46eHl6"}


def test_api_good_request(client):
    res = client.post("/v1/notify/", json=NOTIFY, headers=HEADERS)
    assert res.status_code == 202
    assert res.json() == {"status": "OK", "message": "Notification Accepted!"}
