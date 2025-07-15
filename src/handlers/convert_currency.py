import uuid
from decimal import ROUND_UP, Decimal

from fastapi import HTTPException

from src.db import memory_storage
from src.handlers.update_rates import CURRENCIES


def convert_currency(user_id, currency, new_currency, amount, storage=memory_storage):

    if currency == new_currency:
        raise HTTPException(400, detail='Currencies must be different')

    currency = storage.find_one('currencies', name=currency)
    new_currency = storage.find_one('currencies', name=new_currency)

    if not currency:
        raise HTTPException(404, detail='Currency {} not found'.format(currency))

    if not new_currency:
        raise HTTPException(404, detail='Currency {} not found'.format(new_currency))

    account = storage.find_one('accounts', user_id=user_id, currency_id=currency['id'])

    if not account:
        raise HTTPException(404, detail='Account not found')

    if account['amount'] < amount:
        raise HTTPException(400, detail='Insufficient Balance')

    rounded_up_amount = round_up_amount_to_available_decimal(amount, account['amount'])

    rate = CURRENCIES[currency['name']][new_currency['name']]

    old_account_balance = Decimal(str(account['amount'])) - rounded_up_amount

    print(Decimal(str(account['amount'])) - rounded_up_amount)

    updated_old_account = storage.update(
        'accounts',
        filters={'user_id': user_id, 'currency_id': currency['id']},
        new_values={'amount': old_account_balance}
    )

    new_account = storage.find_one('accounts', user_id=user_id, currency_id=new_currency['id'])

    if not new_account:
        new_account = storage.insert(
            'accounts',
            {'user_id': 1, 'currency_id': new_currency['id'], 'amount': 0}
        )

    new_amount = Decimal(str(new_account['amount'])) + Decimal(str(rate)) * rounded_up_amount

    updated_new_account = storage.update(
        'accounts',
        filters={'user_id': user_id, 'currency_id': new_currency['id']},
        new_values={'amount': new_amount}
    )

    conversion_id = generate_conversion_id()

    storage.insert(
        'transactions',
        {
            'account_id': account['id'],
            'currency_id': currency['id'],
            'amount': amount,
            'type': 'debit',
            'fx_rate': rate,
            'conversion_id': conversion_id,
        }
    )

    storage.insert(
        'transactions',
        {
            'original_currency_id': currency['id'],
            'original_amount': amount,
            'account_id': account['id'],
            'amount': new_amount,
            'currency_id': new_currency['id'],
            'type': 'credit',
            'fx_rate': rate,
            'conversion_id': conversion_id,
        }
    )

    return [updated_old_account, updated_new_account]


def round_up_amount_to_available_decimal(user_input: int, stored_amount: float) -> Decimal:
    stored_decimal = Decimal(str(stored_amount)).quantize(Decimal('0.01'), rounding=ROUND_UP)

    if user_input == int(stored_decimal):
        return stored_decimal
    return Decimal(user_input).quantize(Decimal('0.01'))


def generate_conversion_id():
    return str(uuid.uuid4())
