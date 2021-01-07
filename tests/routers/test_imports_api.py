# Standard library imports
import copy
from typing import Dict

# Third party imports
import pytest
import ujson as json

# Local application imports
from brandenburg.config import settings

xfail = pytest.mark.xfail

DATA: Dict[str, str] = {
    "service_id": "test_brandenburg",
    "table_name": "user",
    "data": [{"id": 1, "name": "Maria", "updated_at": "2020-12-03T19:35:30.0494511"}],
    "action": "upsert",
    "sequence_pointer_field": "updated_at",
}


HEADERS: Dict[str, str] = {
    "Origin": "*/*",
    "Content-Type": "application/json",
    "Authorization": "Basic QURNSU46eHl6",
}


def test_api_good_request(client):
    res = client.post(f"/v1/import/push/", json=DATA, headers=HEADERS)
    assert res.status_code == 201


def test_api_get_400_with_wrong_data(client):
    res = client.post(f"/v1/import/push/", json={"a": 1}, headers=HEADERS)
    assert res.status_code == 422


def test_api_get_401_without_auth(client):
    res = client.post(f"/v1/import/push/", json={"a": 1})
    assert res.status_code == 401


def test_api_with_sequence_field_request(client):
    data: Dict[str, str] = copy.deepcopy(DATA)
    data.update({"sequence_pointer_field": "updated_at"})
    res = client.post(f"/v1/import/push/", json=data, headers=HEADERS)
    assert res.status_code == 201


def test_full_fields(client):
    full: Dict[str, str] = copy.deepcopy(DATA)
    full["key_names"] = ["id"]
    full["schema_mapping"] = [{"name": "id", "type": "int", "is_nullable": True}]
    full["action"] = "batch"
    res = client.post(f"/v1/import/batch/", json=full, headers=HEADERS)
    assert res.status_code == 201


@pytest.mark.xfail
def test_send_action_batch(client):
    pass


@pytest.mark.xfail
def test_schema_mapping_without_key_names(client):
    pass


@pytest.mark.xfail
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


@xfail
def test_check_last_datetime_field(client):
    pass
