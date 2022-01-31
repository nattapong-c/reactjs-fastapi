from pydantic import BaseModel, Field
from .objectid import PyObjectId
from bson import ObjectId
from enum import Enum

class CategoryEnum(str, Enum):
    food="food"
    drink="drink"
    snack="snack"

class Product(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    price: int
    category: CategoryEnum
    stock: int = 0
    image: ObjectId

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
