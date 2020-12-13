# Standard library imports
import copy

# Third party imports
import pytest
import ujson as json
from pydantic import ValidationError

# Local application imports
from brandenburg.models.batch import BatchModel

BATCH = {
    "service_id": "raw",
    "table_name": "users",
    "action": "upsert",
    "data": [{"id": 1, "name": "maria", "email": "maria@uol.in"}],
}


def test_good_data():
    batch: BatchModel = BatchModel(**BATCH)
    assert batch._sdc_received_at is not None
    assert isinstance(batch._sdc_sequence, int) is True
    assert len(batch.key_names) == 0
    assert batch.schema_mapping is None


def test_missing_data_field():
    bad_batch = copy.deepcopy(BATCH)
    bad_batch["data"] = list()
    with pytest.raises(ValidationError) as info:
        batch: BatchModel = BatchModel(**bad_batch)

    assert json.loads(info.value.json()) == [
        {"loc": ["data"], "msg": "Field data cannot be empty.", "type": "value_error",}
    ]


def test_batch_with_schema_mapping():
    params = copy.deepcopy(BATCH)
    params["action"] = "batch"
    params["key_names"] = ["Id"]
    params["schema_mapping"] = [
        {"type": "TIMESTAMP", "name": "LastUpdateDate", "is_nullable": "true"},
        {"type": "INTEGER", "name": "Id", "is_nullable": "true"},
        {"type": "STRING", "name": "Reason", "is_nullable": "true"},
    ]
    batch: BatchModel = BatchModel(**params)
    assert len(batch.schema_mapping) == 3


def test_batch_missing_schema():
    bad_batch = copy.deepcopy(BATCH)
    bad_batch["action"] = "batch"
    with pytest.raises(ValidationError) as info:
        batch: BatchModel = BatchModel(**bad_batch)

    assert json.loads(info.value.json()) == [
        {
            "loc": ["action"],
            "msg": "Fields schema_mapping and key_names cannot be empty when action is batch",
            "type": "value_error",
        }
    ]


def test_with_data_over_1000():
    bad_batch = copy.deepcopy(BATCH)
    bad_batch["data"] = [bad_batch["data"][0] for _ in range(1001)]
    with pytest.raises(ValidationError) as info:
        batch: BatchModel = BatchModel(**bad_batch)

    assert json.loads(info.value.json()) == [
        {"loc": ["data"], "msg": "Field data exceed 1000 records.", "type": "value_error",}
    ]
