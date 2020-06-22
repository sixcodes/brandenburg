import pytest
from pydantic import ValidationError

from brandenburg.models.lead import LeadModel


def test_good_data():

    lead = LeadModel(
        name="Maria Silva", phone_number="55912345678", email="maria@gmail.com", is_term_accepted="True", origin="lpx"
    )
    assert lead == {
        "name": "Maria Silva",
        "phone_number": "55912345678",
        "email": "maria@gmail.com",
        "group": "A",
        "is_term_accepted": "True",
        "origin": "lpx",
        "by": "salesforce",
    }


def test_with_group_A():
    lead = LeadModel(
        name="Maria Silva", phone_number="55912345678", email="maria@gmail.com", is_term_accepted="True", origin="lpx"
    )
    assert lead.group == "A"


def test_with_group_A_yahoo():
    lead = LeadModel(
        name="Maria Silva", phone_number="55912345678", email="maria@yahoo.it", is_term_accepted="True", origin="lpx"
    )
    assert lead.group == "A"


def test_with_group_B():
    lead = LeadModel(
        name="Maria Silva",
        phone_number="55912345678",
        email="maria@apolloagricola.com.br",
        is_term_accepted="True",
        origin="lpx",
    )
    assert lead.group == "B"


def test_raise_error_with_wrong_name():
    with pytest.raises(ValidationError) as ex:
        LeadModel(name="M", phone_number="55912345678", email="maria@apolloagricola.com.br")


def test_raise_error_with_short_phone_number():
    with pytest.raises(ValidationError) as ex:
        LeadModel(name="Maria Silva", phone_number="345678", email="maria@apolloagricola.com.br")


def test_raise_error_with_wrong_email():
    with pytest.raises(ValidationError) as ex:
        LeadModel(name="Maria Silva", phone_number="55912345678", email="maria@yahoo.")


def test_raise_error_with_letter_in_phone_number():
    with pytest.raises(ValidationError) as ex:
        LeadModel(name="Maria Silva", phone_number="aa912345678", email="maria@yahoo.com")
