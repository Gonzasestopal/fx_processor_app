from pydantic import BaseModel


class WithdrawRequest(BaseModel):
    currency: str
    amount: int
