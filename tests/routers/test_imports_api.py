import copy
from typing import Dict

import pytest
import ujson as json

from brandenburg.config import settings

DATA: Dict[str, str] = {
    "service_id": "partner1",
    "table_name": "user",
    "data": [{"id": 1, "name": "Maria"}],
    "action": "upsert",
}


HEADERS: Dict[str, str] = {"Origin": "*/*", "Content-Type": "application/json", "Authorization": "Basic QURNSU46eHl6"}


def test_api_good_request(client):
    res = client.post(f"/v1/import/push/", json=DATA, headers=HEADERS)
    assert res.status_code == 201


def test_api_get_400_with_wrong_data(client):
    res = client.post(f"/v1/import/push/", json={"a": 1}, headers=HEADERS)
    assert res.status_code == 422


@pytest.mark.xfail
def test_full_fields(client):
    full: Dict[str, str] = copy.deepcopy(DATA)
    full["key_names"] = ["id"]
    full["schema_mapping"] = [{"a": "s"}]
    pass


@pytest.mark.xfail
def test_send_action_batch(client):
    pass


@pytest.mark.xfail
def test_schema_mapping_without_key_names(client):
    pass


@pytest.mark.fail
def test_send_empty_values(client):
    pass


@pytest.mark.xfail
def test_send_more_than_10k_records(client):
    pass


@pytest.mark.xfail
def test_send_file_ok(client):
    pass


@pytest.mark.xfail
def test_send_empty_file_param(client):
    pass


@pytest.mark.xfail
def test_send_file_and_check_background_function(client):
    """
    Check if the files was uploaded
    """
    pass
