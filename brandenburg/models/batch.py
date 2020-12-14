# Standard library imports
from datetime import datetime
from typing import List, Dict, Union, Optional

# Third party imports
from pydantic import BaseModel, PrivateAttr, Field, validator

# Local application imports
from brandenburg.config import settings

BATCH_LIMIT: int = settings.BATCH_LIMIT


class ImportResponse(BaseModel):
    status: str = Field(..., title="Status of response", choices=(("ok", "error")))
    message: str
    token: str = Field(..., title="A token to authenticate/validate the request postpone")


class SchemaMapping(BaseModel):
    """
    :param type:
    :param name:
    :param is_nullable:

    Eg:
        {"type": "STRING", "name": "document_number", "is_nullable": true}
    """

    type: str = Field(title="Column data type. E.g: numeric, decimal, float, varchar, date")
    name: str = Field(title="Column Name on the database")
    is_nullable: bool = Field(title="If the column can be NULL", default=True)


class BatchModel(BaseModel):
    service_id: str = Field(
        ...,
        title="""The microservice ID. The service ID associated with your Service. This information was send to you tochether with your credentials""",
    )
    table_name: str = Field(
        ...,
        title="""The name of the destination table the data is being pushed to. Table names must be unique in each destination schema, or loading issues will occur. A single request can push data to multiple tables.""",
    )
    data: List[Dict[str, Union[str, float, datetime, int, bool, None]]] = Field(
        ...,
        title="""An object representing a record to be pushed into the destination table.""",
        min_items=1,
        max_items=BATCH_LIMIT,
    )
    key_names: Optional[List[str]] = Field(
        list(), title="""An array of strings representing the Primary Key fields in the destination table.""",
    )
    schema_mapping: Optional[List[SchemaMapping]]  # = Field(list({}), title="""The table schema""")
    action: str = Field(
        title="This will always be upsert.", choices=(("upsert", "batch")), default="upsert",
    )
    _sdc_received_at: str = PrivateAttr()
    _sdc_sequence: int = PrivateAttr()

    def __init__(self, **kwargs) -> None:
        """
        :param service_id:
        :param table_name:
        :param action:
        :param sdc_sequence: An integer that tells the Import API the order in which data points in the request body should be
        considered for loading. This data will be stored in the destination table in the _sequence column.
        This API uses a Unix epoch (in milliseconds) as the value for this property.
        Note: This value cannot exceed the maximum of 9223372036854775807.
        """
        # import ipdb; ipdb.set_trace()
        super().__init__(**kwargs)
        NOW: datetime = datetime.now()
        self._sdc_received_at = NOW.strftime("%y-%m-%d %H:%M:%S")
        self._sdc_sequence = int(NOW.timestamp())

    @validator("data", pre=True)
    def data_validator(cls, value):
        """
        """
        if isinstance(value, list):
            if len(value) > BATCH_LIMIT:
                raise ValueError(f"Field data exceed {BATCH_LIMIT} records.")
            if not len(value):
                raise ValueError("Field data cannot be empty.")
        return value

    @validator("action", always=True)
    def action_validator(cls, value, values):
        if value == "batch":
            if not values["schema_mapping"] or not len(values["key_names"]):
                raise ValueError("Fields schema_mapping and key_names cannot be empty when action is batch")

    # @validator("key_names", pre=True, always=True)
    # def key_names_validator(cls, value, values):
    #     assert isinstance(value, list) == True
    #     if not len(value):
    #         raise ValueError("Field key_names cannot be empty")

    #     import ipdb; ipdb.set_trace()
    #     keys: Set[str] = {k for k in values["data"].keys()}
    #     if not len([key in keys for key in value]):
    #         raise ValueError("Fields on key_names must be into data.")
    # return value
