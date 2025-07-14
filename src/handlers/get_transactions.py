from fastapi import HTTPException

from src.db import memory_storage


def get_transactions(user_id, storage=memory_storage):
    account = storage.find_one('accounts', user_id=user_id)

    if not account:
        raise HTTPException(status_code=404, detail='Account not found')

    transactions = storage.find('transactions', account_id=account['id'])

    return transactions
