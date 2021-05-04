# Standard library imports
from enum import Enum
from typing import Union, Dict

# Third party imports
from pydantic import BaseModel, ValidationError, EmailStr, Field, validator

# TODO: A great candidate to be a protobuffer file


class ByEnum(str, Enum):
    sms = "sms"
    whatsapp = "whatsapp"
    email = "email"


class NotifyModel(BaseModel):
    contact: Union[EmailStr, str] = Field(..., title="The contact email or phone number")
    by: ByEnum = Field(..., title="Which pipe it should be send")
    data: Dict[str, Union[int, str, float]] = Field(..., title="Data to be used into template")
    template_name: str = Field(..., title="Template name")
    locale: str = Field("pt-BR", title="Locale")

    @validator("data", pre=True)
    def data_validator(cls, value):
        """"""
        assert isinstance(value, dict) == True
        if not value:
            raise ValueError("Field data cannot be empty.")
        return value
