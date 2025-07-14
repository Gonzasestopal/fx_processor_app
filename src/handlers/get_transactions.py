from fastapi import HTTPException

from src.db import memory_storage


def get_transactions(user_id, storage=memory_storage):
    accounts = storage.find('accounts', user_id=user_id)

    if not accounts:
        raise HTTPException(status_code=404, detail='Account not found')

    response = []

    for account in accounts:
        transactions = storage.find('transactions', account_id=account['id'])
        response.extend(transactions)

    return response
