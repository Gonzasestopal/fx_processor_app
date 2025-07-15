from decimal import ROUND_CEILING, ROUND_HALF_UP, Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator

from src.db import Memory


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

    class Meta:
        unique_together = ('user_id', 'currency_id',)

    @field_validator("amount", mode="before")
    @classmethod
    def round_float_to_int(cls, v):
        if isinstance(v, Decimal):
            return int(Decimal(str(v)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        return v


class TransactionType(str, Enum):
    debit = "debit"
    credit = "credit"


class Transaction(BaseModel):
    id: int
    account_id: int
    currency_id: int
    amount: int
    type: TransactionType
    original_currency_id:  Optional[int] = None
    original_amount:  Optional[int] = None
    fx_rate: Optional[float] = None

    @model_validator(mode="after")
    def set_original_fields(self):
        if self.original_currency_id is None:
            self.original_currency_id = self.currency_id
        if self.original_amount is None:
            self.original_amount = self.amount
        return self


Memory.register_model("accounts", Account)
