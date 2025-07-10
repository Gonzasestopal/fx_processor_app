from fastapi import HTTPException

from src.db import memory_storage


def convert_currency(user_id, currency, new_currency, amount, storage=memory_storage):

    if currency == new_currency:
        raise HTTPException(400, detail='Currencies must be different')

    currency = storage.find_one('currency', currency=currency)
    new_currency = storage.find_one('currency', currency=new_currency)

    if not currency:
        raise HTTPException(404, detail='Currency {} not found'.format(currency))

    if not new_currency:
        raise HTTPException(404, detail='Currency {} not found'.format(new_currency))

    return True
