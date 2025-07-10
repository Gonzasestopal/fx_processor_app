
from typing import List

from fastapi import APIRouter

from src import handlers
from src.models import Account
from src.requests import ConvertRequest, FundRequest

router = APIRouter()


@router.post('/{user_id}/fund', response_model=Account)
def fund_account(user_id: int, request: FundRequest):
    return handlers.fund_account(user_id, amount=request.amount, currency=request.currency)


@router.post('/{user_id}/convert', response_model=List[Account])
def convert_currency(user_id: int, request: ConvertRequest):
    return handlers.convert_currency(
        user_id,
        amount=request.amount,
        currency=request.currency,
        new_currency=request.new_currency,
    )
