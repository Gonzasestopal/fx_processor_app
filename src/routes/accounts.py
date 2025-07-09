
from fastapi import APIRouter

from src import handlers
from src.models import Account
from src.requests import FundRequest

router = APIRouter()


@router.post('/{user_id}/fund', response_model=Account)
def fund_account(user_id: int, request: FundRequest):
    return handlers.fund_account(user_id, amount=request.amount, currency=request.currency)
