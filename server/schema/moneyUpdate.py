from enum import IntEnum
from pydantic import BaseModel
from typing import Optional

class AmountEnum(IntEnum):
    b1 = 1
    b5 = 5
    b10 = 10
    b20 = 20
    b50 = 50
    b100 = 100
    b500 = 500
    b1000 = 1000


class MoneyUpdate(BaseModel):
    amount: Optional[AmountEnum]
    stock: Optional[int]
