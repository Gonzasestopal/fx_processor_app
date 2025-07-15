from fastapi import HTTPException

from src.db import memory_storage


def fund_account(user_id: int, currency: str, amount: int, storage=memory_storage):
    currency = storage.find_one('currencies', name=currency)

    if not currency:
        raise HTTPException(404, detail='Currency {} not found'.format(currency))

    account = storage.find_one('accounts', user_id=user_id, currency_id=currency['id'])

    if not account:
        account = storage.insert(
            'accounts',
            {'amount': amount, 'user_id': user_id, 'currency_id': currency['id']}
        )

        storage.insert(
            'transactions',
            {
                'account_id': account['id'],
                'amount': amount,
                'currency_id': currency['id'],
                'type': 'credit',
            }
        )

        return account

    new_amount = account['amount'] + amount

    updated_account = storage.update(
        'accounts',
        filters={'user_id': user_id, 'currency_id': currency['id']},
        new_values={'amount': new_amount},
    )

    storage.insert(
        'transactions',
        {
            'account_id': account['id'],
            'amount': amount,
            'currency_id': currency['id'],
            'type': 'credit',
        }
    )

    return updated_account
