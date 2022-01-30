from enum import IntEnum
from pydantic import BaseModel, Field
from .objectid import PyObjectId
from bson import ObjectId

class AmountEnum(IntEnum):
    b1 = 1
    b5 = 5
    b10 = 10
    b20 = 20
    b50 = 50
    b100 = 100
    b500 = 500
    b1000 = 1000


class Money(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    amount: AmountEnum
    stock: int = 0

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
