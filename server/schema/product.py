from pydantic import BaseModel, Field
from .objectid import PyObjectId
from bson import ObjectId


class Product(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    price: int
    category: str
    stock: int = 0
    image: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
