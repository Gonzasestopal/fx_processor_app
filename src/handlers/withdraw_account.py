
from fastapi import HTTPException

from src.db import memory_storage


def withdraw_account(user_id: int, currency: str, amount: int, storage=memory_storage):

    currency = storage.find_one('currencies', name=currency)

    if not currency:
        raise HTTPException(status_code=404, detail='Currency {} not found'.format(currency))

    account = storage.find_one('accounts', user_id=user_id, currency_id=currency['id'])

    if not account:
        raise HTTPException(status_code=404, detail='Account not found')

    if account['amount'] < amount:
        raise HTTPException(status_code=400, detail='Insufficient Balance')

    new_amount = account['amount'] - amount

    updated_account = storage.update(
        'accounts',
        filters={'user_id': user_id, 'currency_id': currency['id']},
        new_values={'amount': new_amount},
    )

    return updated_account
