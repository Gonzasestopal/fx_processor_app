from fastapi import HTTPException

from src.db import memory_storage
from src.models import Account


def view_balances(user_id, storage=memory_storage):
    accounts = storage.find('accounts', user_id=user_id)

    if not accounts:
        raise HTTPException(status_code=404, detail='Account not found')

    response = {}

    for account in accounts:
        currency = storage.find_one('currencies', id=account['currency_id'])
        response[currency['name']] = Account.round_amount(account['amount'])

    return response
