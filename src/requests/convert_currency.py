from pydantic import BaseModel


class ConvertRequest(BaseModel):
    currency: str
    new_currency: str
    amount: int
