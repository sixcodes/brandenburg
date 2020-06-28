import copy
from typing import Dict, Union

import pytest
import ujson as json
from pydantic import EmailStr, ValidationError

from brandenburg.models.notify import NotifyModel

NOTIFY: Dict[str, Union[str, EmailStr]] = {
    "contact": "abc@admin.com",
    "by": "sms",
    "template_name": "password_reset",
    "data": {"subject": "New password", "password": "abc123"},
}


def test_good_data():
    notify: NotifyModel = NotifyModel(**NOTIFY)
    assert notify == {
        "contact": "abc@admin.com",
        "by": "sms",
        "template_name": "password_reset",
        "data": {"subject": "New password", "password": "abc123"},
        "locale": "pt-BR",
    }


def test_missing_contact():
    bad_notify = copy.deepcopy(NOTIFY)
    del bad_notify["contact"]
    with pytest.raises(ValidationError) as info:
        notify: NotifyModel = NotifyModel(**bad_notify)
    assert json.loads(info.value.json()) == [
        {'loc': ['contact'], 'msg': 'field required', 'type': 'value_error.missing'}
    ]


def test_with_wrong_by_option():
    bad_notify = copy.deepcopy(NOTIFY)
    bad_notify["by"] = "xyz"
    with pytest.raises(ValidationError) as info:
        notify: NotifyModel = NotifyModel(**bad_notify)
    assert json.loads(info.value.json()) == [
        {
            'loc': ['by'],
            'msg': "value is not a valid enumeration member; permitted: 'sms', 'whatsapp', 'email'",
            'type': 'type_error.enum',
            'ctx': {'enum_values': ['sms', 'whatsapp', 'email']},
        }
    ]


def test_empty_data():
    bad_notify = copy.deepcopy(NOTIFY)
    bad_notify["data"] = {}
    with pytest.raises(ValidationError) as info:
        notify: NotifyModel = NotifyModel(**bad_notify)
    assert json.loads(info.value.json()) == [
        {'loc': ['data'], 'msg': 'Field data cannot be empty.', 'type': 'value_error'}
    ]


def test_data_wrong_type():
    bad_notify = copy.deepcopy(NOTIFY)
    bad_notify["data"] = []
    with pytest.raises(ValidationError) as info:
        notify: NotifyModel = NotifyModel(**bad_notify)
    assert json.loads(info.value.json()) == [{'loc': ['data'], 'msg': '', 'type': 'assertion_error'}]
