from pydantic import BaseModel, Field
from typing import Dict


class UsedMoney():
    __root__: Dict[str, int]


class Payment(BaseModel):
    product_id: str
    used_money: UsedMoney

    class Config:
        arbitrary_types_allowed = True
