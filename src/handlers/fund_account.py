from fastapi import HTTPException

from src.db import memory_storage
from src.requests import FundRequest


def fund_account(user_id: int, request: FundRequest):
    currency = memory_storage.find_one('currencies', name=request.currency)

    if not currency:
        raise HTTPException(404, detail='Currency {} not found'.format(request.currency))

    account = memory_storage.find_one('accounts', user_id=user_id, currency_id=currency['id'])

    print(account)

    if not account:
        return memory_storage.insert(
            'accounts',
            {'amount': request.amount, 'user_id': user_id, 'currency_id': currency['id']}
        )

    new_amount = account['amount'] + request.amount

    updated_account = memory_storage.update('accounts', filters={'user_id': user_id, 'currency_id': currency['id']}, new_values={'amount': new_amount})

    print(updated_account, 'updated')

    return updated_account
