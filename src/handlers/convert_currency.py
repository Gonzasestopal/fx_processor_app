from types import MappingProxyType

from fastapi import HTTPException

from src.db import memory_storage

MXN_CONVERSION_RATES = MappingProxyType({
    'USD': 0.053
})

USD_CONVERSION_RATES = MappingProxyType({
    'MXN': 18.70
})

CURRENCIES = MappingProxyType({
    'MXN': MXN_CONVERSION_RATES,
    'USD': USD_CONVERSION_RATES,
})


def convert_currency(user_id, currency, new_currency, amount, storage=memory_storage):

    if currency == new_currency:
        raise HTTPException(400, detail='Currencies must be different')

    currency = storage.find_one('currency', currency=currency)
    new_currency = storage.find_one('currency', currency=new_currency)

    if not currency:
        raise HTTPException(404, detail='Currency {} not found'.format(currency))

    if not new_currency:
        raise HTTPException(404, detail='Currency {} not found'.format(new_currency))

    account = storage.find_one('accounts', user_id=user_id, currency_id=currency['id'])

    if not account:
        raise HTTPException(404, detail='Account not found')

    if account['amount'] < amount:
        raise HTTPException(400, detail='Insufficient Balance')

    rate = CURRENCIES[currency['name']][new_currency['name']]

    old_account_balance = account['amount'] - amount

    updated_old_account = storage.update(
        'accounts',
        filters={'user_id': user_id, 'currency_id': currency['id']},
        new_values={'amount': old_account_balance}
    )

    new_account = storage.find_one('accounts', user_id=user_id, currency_id=new_currency['id'])

    if not new_account:
        new_account = storage.insert(
            'accounts',
            {'user_id': 1, 'currency_id': new_currency['id'], amount: 0}
        )
        print(new_account)

    updated_new_account = storage.update(
        'accounts',
        filters={'user_id': user_id, 'currency_id': new_currency['id']},
        new_values={'amount': new_account['amount'] + rate * amount}
    )

    print(updated_new_account, new_account['amount'], rate, amount)

    return [updated_old_account, updated_new_account]
