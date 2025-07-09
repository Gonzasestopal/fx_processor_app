from pydantic import BaseModel


class FundRequest(BaseModel):
    currency: str
    amount: int
