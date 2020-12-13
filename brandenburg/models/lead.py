# Standard library imports
from typing import Tuple, List

# Third party imports
from pydantic import BaseModel, validator, EmailStr, Field

# @doc.consumes(
#     doc.JsonBody(
#         {
#             "name": doc.String("The name of the user."),
#             "phone_number": doc.String("The user phone number."),
#             "email": doc.String("The euser email."),
#             "is_term_accepted": doc.String("If user accepted the term of privacy."),
#             "origin": doc.String("The lead origin."),
#             "outcome": doc.String("Where this data should be sent."),
#         }
#     ),
#     location="body",
# )
#


class LeadModel(BaseModel):
    name: str
    phone_number: str
    email: EmailStr
    group: str
    is_term_accepted: str
    origin: str
    role: str = ""
    by: str = "salesforce"

    def __init__(self, name: str, phone_number: str, email: EmailStr, **data) -> None:
        """"""
        group: str = self.__get_group(email)
        super().__init__(
            name=name, phone_number=phone_number, email=email, group=group, **data,
        )

    @validator("name", pre=True, always=True)
    def name_validator(cls, value):
        if len(value) < 3:
            raise ValueError("Name is invalid")
        return value

    @validator("phone_number", pre=True, always=True)
    def phone_number_validator(cls, value):
        """
        TODO: Use phonenumbers lib to validate phone numbers
        """
        assert isinstance(int(value), int) == True

        if len(value) < 11:
            raise ValueError("Invalid phone number")
        return value

    def __get_group(self, email) -> str:
        providers: List[str] = [
            "gmail.com",
            "g1.com",
            "hotmail.com",
            "icloud.com",
            "ig.com.br",
            "bol.com.br",
            "aol.com.br",
            "globo.com",
            "protonmail.com",
            "r7.com",
            "terra.com",
            "terra.com.br",
            "uol.com.br",
            "uol.com",
            "vivo.com.br",
            "yahoo.",
            "live.com",
            "zipmail.com",
            "zipmail.com.br",
            "lycos.com",
            "mail.com",
            "outlook.com",
            "msn.com.br",
            "yandex.com",
            "gmx.com",
            "gmx.us",
            "zohomail.eu",
        ]
        for item in providers:
            if email.find(item) > 0:
                return "A"

        return "B"
