from enum import Enum, IntEnum

from pydantic import BaseModel, ValidationError, EmailStr


class ByEnum(str, Enum):
    sms = 'sms'
    whatsapp = 'whatsapp'
    email = 'email'
    salesforce = "salesforce"


class NotifyModel(BaseModel):
    contact: Union[EmailStr, str] = Field(..., title="x")
    by: ByEnum = Field(..., title="c")
    data: Dict[str, Union[int, str, float]] = Field(..., title="")
    template_name: str = Field(..., title="t")
    locale: str = Field("pt_BR", title="Locale")
