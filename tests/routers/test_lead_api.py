import asyncio
import json

import aioredis
import pytest
from pydantic import ValidationError

from brandenburg.config import settings

LEAD = {
    "name": "Maria Silva",
    "phone_number": "55912345678",
    "email": "maria@gmail.com",
    "is_term_accepted": "True",
    "origin": "lpx",
}

headers = {"Origin": "*/*"}


def test_get_token(client):
    res = client.get("/v1/leads/token/", headers=headers)
    res_json = res.json()
    assert res.status_code == 200
    assert len(res_json.get("token")) == 36


def test_api_good_request(client):
    get_token = client.get("/v1/leads/token/", headers=headers)
    result = get_token.json()
    res = client.post(f"/v1/leads/{result.get('token')}/", json=LEAD, headers=headers)
    assert res.status_code == 201


def test_api_wrong_path_request(client):
    res = client.get("/leads/ab123/", headers=headers)
    assert res.status_code == 404


def test_api_get_422_with_wrong_data(client):
    get_token = client.get("/v1/leads/token/", headers=headers)
    result = get_token.json()
    res = client.post(f"/v1/leads/{result.get('token')}/", json={"a": 1})
    assert res.status_code == 422


def test_api_get_307_with_wrong_path(client):
    get_token = client.get("/v1/leads/token/", headers=headers)
    result = get_token.json()
    res = client.post(f"/v1/leads/{result.get('token')}", json={"a": 1})
    assert res.status_code == 307


def test_api_get_400_with_wrong_token(client):
    res = client.post(f"/v1/leads/234234fsdfsdf/", json=LEAD)
    assert res.status_code == 400


@pytest.mark.xfail
def test_send_wrong_data_match_error(client):
    pass
