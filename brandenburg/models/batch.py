from datetime import datetime
from typing import Tuple, List, Dict, Union, Set, Optional

from pydantic import BaseModel, Field, Json, validator, root_validator

BATCH_LIMIT: int = 10000


class SchemaMapping(BaseModel):
    type: str = Field(title="Column data type", default="")
    name: str = Field(title="Name", default="")
    is_nullable: bool = Field(title="xyz", default=True)


class BatchModel(BaseModel):
    service_id: str = Field(
        ...,
        title="""The microservice ID. The service ID associated with your Service. This information was send to you tochether with your credentials""",
    )
    table_name: str = Field(
        ...,
        title="""The name of the destination table the data is being pushed to. Table names must be unique in each destination schema, or loading issues will occur. A single request can push data to multiple tables.""",
    )
    data: List[Dict[str, Union[str, float, datetime, int, bool]]] = Field(
        ...,
        title="""An object representing a record to be pushed into the destination table.""",
        min_items=1,
        max_items=BATCH_LIMIT,
    )
    action: str = Field("upsert", title="This will always be upsert.", choices=(("upsert", "batch")))
    sdc_received_at: Optional[str]
    sdc_sequence: Optional[int]
    key_names: Optional[List[str]] = Field(
        list(), title="""An array of strings representing the Primary Key fields in the destination table."""
    )
    schema_mapping: Optional[List[SchemaMapping]] = Field(list(), title="""The table schema""")

    def __init__(
        self,
        service_id: str,
        table_name: str,
        action: str,
        data: List[Dict[str, Union[str, float, datetime, int, bool]]],
        **kwargs,
    ) -> None:
        """
        param: sdc_sequence An integer that tells the Import API the order in which data points in the request body should be
        considered for loading. This data will be stored in the destination table in the _sequence column.
        This API uses a Unix epoch (in milliseconds) as the value for this property.
        Note: This value cannot exceed the maximum of 9223372036854775807. 
        """
        NOW: datetime = datetime.now()
        _sdc_received_at: str = NOW.strftime('%y-%m-%d %I:%M:%S')
        _sdc_sequence: int = int(NOW.timestamp())
        super().__init__(
            service_id=service_id,
            table_name=table_name,
            action=action,
            data=data,
            sdc_sequence=_sdc_sequence,
            sdc_received_at=_sdc_received_at,
            **kwargs,
        )

    @validator("data", pre=True)
    def data_validator(cls, value):
        """
        """
        assert isinstance(value, list) == True
        if len(value) > BATCH_LIMIT:
            raise ValueError("Field data exceed 10000 records.")
        if not len(value):
            raise ValueError("Field data cannot be empty.")
        return value

    # @validator("schema_mapping")
    # def schema_mapping_validator(cls, value, values):
    #     if "key_names" in values:
    #     # import ipdb; ipdb.set_trace()
    #         if not len(values["key_names"]) or not len(value):
    #             raise ValueError("Field key_names cannot be empty when there is schema mapping")

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
