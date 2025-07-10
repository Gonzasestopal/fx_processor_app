from fastapi import HTTPException

from src.db import memory_storage


def convert_currency(user_id, currency, new_currency, amount, storage=memory_storage):
    currency = storage.find_one('currency', currency=currency)

    if not currency:
        raise HTTPException(404, detail='Currency {} not found'.format(currency))

    return True
