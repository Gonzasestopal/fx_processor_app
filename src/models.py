from decimal import ROUND_HALF_UP, Decimal

from pydantic import BaseModel, field_validator


class User(BaseModel):
    id: int


class Currency(BaseModel):
    id: int
    name: str


class Account(BaseModel):
    id: int
    user_id: int
    currency_id: int
    amount: int

    @field_validator("amount", mode="before")
    @classmethod
    def round_float_to_int(cls, v):
        if isinstance(v, float):
            return int(Decimal(str(v)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        return v
