
from decimal import Decimal
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from src.handlers.convert_currency import (
    convert_currency, round_up_amount_to_available_decimal)


def test_convert_currency_mxn():
    user_id = 1
    currency = 'MXN'
    new_currency = 'USD'
    amount = 100
    storage = Mock()
    account = {'amount': 100}
    new_account = {'amount': 0}

    mxn_currency = {'id': 1, 'name': 'MXN'}
    usd_currency = {'id': 2, 'name': 'USD'}
    storage.find_one.side_effect = [mxn_currency, usd_currency, account, new_account]
    storage.update.side_effect = [
        {'amount': account['amount'] - amount},
        {'amount': new_account['amount'] + account['amount'] * 0.053}
    ]

    accounts = convert_currency(user_id, currency, new_currency, amount, storage)

    assert accounts[1]['amount'] == (amount * 0.053)


def test_convert_currency_usd():
    user_id = 1
    currency = 'USD'
    new_currency = 'MXN'
    amount = 100
    storage = Mock()
    account = {'amount': 100}
    new_account = {'amount': 0}

    mxn_currency = {'id': 1, 'name': 'MXN'}
    usd_currency = {'id': 2, 'name': 'USD'}
    storage.find_one.side_effect = [mxn_currency, usd_currency, account, new_account]
    storage.update.side_effect = [
        {'amount': account['amount'] - amount},
        {'amount': new_account['amount'] + account['amount'] * 18.70}
    ]
    accounts = convert_currency(user_id, currency, new_currency, amount, storage)

    assert accounts[1]['amount'] == (amount * 18.70)


def test_currency_not_found():
    user_id = 1
    currency = 'JPN'
    new_currency = 'MXN'
    amount = 100
    storage = Mock()
    storage.find_one.return_value = None

    with pytest.raises(HTTPException):
        convert_currency(user_id, currency, new_currency, amount, storage)


def test_new_currency_not_found():
    user_id = 1
    currency = 'USD'
    new_currency = 'JPN'
    amount = 100
    storage = Mock()
    storage.find_one.return_value = None

    with pytest.raises(HTTPException):
        convert_currency(user_id, currency, new_currency, amount, storage)


def test_currencies_are_equal():
    user_id = 1
    currency = 'USD'
    new_currency = 'USD'
    amount = 100
    storage = Mock()
    storage.find_one.return_value = None

    with pytest.raises(HTTPException):
        convert_currency(user_id, currency, new_currency, amount, storage)


def test_insufficient_balance():
    user_id = 1
    currency = 'USD'
    new_currency = 'MXN'
    amount = 100
    storage = Mock()
    account = {'amount': 99}

    mxn_currency = {'id': 1}
    usd_currency = {'id': 2}
    storage.find_one.side_effect = [usd_currency, mxn_currency, account]

    with pytest.raises(HTTPException):
        convert_currency(user_id, currency, new_currency, amount, storage)


def test_account_not_found():
    user_id = 1
    currency = 'USD'
    new_currency = 'MXN'
    amount = 100
    storage = Mock()
    mxn_currency = {'id': 1}
    usd_currency = {'id': 2}
    storage.find_one.side_effect = [usd_currency, mxn_currency, None]

    with pytest.raises(HTTPException):
        convert_currency(user_id, currency, new_currency, amount, storage)


def test_old_account_balance():
    user_id = 1
    currency = 'MXN'
    new_currency = 'USD'
    amount = 100
    storage = Mock()
    account = {'amount': 100}
    new_account = {'amount': 0}

    mxn_currency = {'id': 1, 'name': 'MXN'}
    usd_currency = {'id': 2, 'name': 'USD'}
    storage.find_one.side_effect = [mxn_currency, usd_currency, account, new_account]
    storage.update.return_value = {'amount': account['amount'] - amount}

    accounts = convert_currency(user_id, currency, new_currency, amount, storage)

    assert accounts[0]['amount'] == account['amount'] - amount


def test_new_account_not_exist():
    user_id = 1
    currency = 'MXN'
    new_currency = 'USD'
    amount = 100
    storage = Mock()
    account = {'amount': 100}
    new_account = None

    mxn_currency = {'id': 1, 'name': 'MXN'}
    usd_currency = {'id': 2, 'name': 'USD'}
    storage.find_one.side_effect = [mxn_currency, usd_currency, account, new_account]
    storage.update.side_effect = [
        {'amount': account['amount'] - amount},
        {'amount': 0 + account['amount'] * 0.053}
    ]

    storage.insert.return_value = {
        'id': 2, 'user_id': 1, 'amount': 2,
    }

    accounts = convert_currency(user_id, currency, new_currency, amount, storage)

    assert accounts[0]['amount'] == 0
    assert accounts[1]['amount'] == (amount * 0.053)


def test_new_account_balance():
    user_id = 1
    currency = 'MXN'
    new_currency = 'USD'
    amount = 100
    storage = Mock()
    account = {'amount': 100}
    new_account = {'amount': 99}

    mxn_currency = {'id': 1, 'name': 'MXN'}
    usd_currency = {'id': 2, 'name': 'USD'}
    storage.find_one.side_effect = [mxn_currency, usd_currency, account, new_account]
    storage.update.side_effect = [
        {'amount': account['amount'] - amount},
        {'amount': new_account['amount'] + account['amount'] * 0.053}
    ]

    accounts = convert_currency(user_id, currency, new_currency, amount, storage)

    assert accounts[1]['amount'] == (new_account['amount'] + amount * 0.053)


def test_convert_to_new_currency_with_floating_point():
    user_id = 1
    currency = 'USD'
    new_currency = 'MXN'
    amount = 5
    storage = Mock()
    account = {'amount': 5.3}
    new_account = {'amount': 0}

    mxn_currency = {'id': 1, 'name': 'MXN'}
    usd_currency = {'id': 2, 'name': 'USD'}
    storage.find_one.side_effect = [mxn_currency, usd_currency, account, new_account]
    rounded_up_amount = round_up_amount_to_available_decimal(amount, account['amount'])
    storage.update.side_effect = [
        {'amount': Decimal(str(account['amount'])) - rounded_up_amount},
        {'amount': Decimal(str(new_account['amount'])) + rounded_up_amount * Decimal('18.70')}
    ]

    accounts = convert_currency(user_id, currency, new_currency, amount, storage)

    assert accounts[0]['amount'] == 0
    assert accounts[1]['amount'] == Decimal('100')


def test_convert_currency_return_value():
    user_id = 1
    currency = 'MXN'
    new_currency = 'USD'
    amount = 100
    storage = Mock()
    account = {'id': 1, 'user_id': 1, 'amount': 100}
    new_account = {'id': 2, 'user_id': 1, 'amount': 99}

    mxn_currency = {'id': 1, 'name': 'MXN'}
    usd_currency = {'id': 2, 'name': 'USD'}
    storage.find_one.side_effect = [mxn_currency, usd_currency, account, new_account]
    storage.update.side_effect = [
        {**account, 'amount': account['amount'] - amount},
        {**new_account, 'amount': new_account['amount'] + account['amount'] * 0.053}
    ]

    accounts = convert_currency(user_id, currency, new_currency, amount, storage)

    updated_account = {'id': 1, 'user_id': 1, 'amount': account['amount'] - amount}
    updated_new_Account = {'id': 2, 'user_id': 1, 'amount': new_account['amount'] + account['amount'] * 0.053}

    assert isinstance(accounts, list)
    assert updated_account in accounts
    assert updated_new_Account in accounts


def test_new_transaction_on_conversion():
    user_id = 1
    currency = 'MXN'
    mxn_currency_id = 1
    usd_currency_id = 2
    new_currency = 'USD'
    amount = 100
    storage = Mock()
    account = {'id': 1, 'user_id': 1, 'amount': 100}
    new_account = {'id': 2, 'user_id': 1, 'amount': 99}

    mxn_currency = {'id': mxn_currency_id, 'name': 'MXN'}
    usd_currency = {'id': usd_currency_id, 'name': 'USD'}

    old_amount = account['amount'] - amount
    new_amount = new_account['amount'] + account['amount'] * 0.053
    storage.find_one.side_effect = [mxn_currency, usd_currency, account, new_account]
    storage.update.side_effect = [
        {**account, 'amount': old_amount},
        {**new_account, 'amount': new_amount}
    ]

    convert_currency(user_id, currency, new_currency, amount, storage)

    first_call_args, first_call_kwargs = storage.insert.call_args_list[0]

    second_call_args, second_call_kwargs = storage.insert.call_args_list[1]

    assert first_call_args == (
        'transactions',
        {
            'account_id': 1,
            'currency_id': mxn_currency_id,
            'amount': amount,
            'type': 'debit',
            'fx_rate': 0.053,
        }
    )

    assert second_call_args == (
        'transactions',
        {
            'original_currency_id': mxn_currency_id,
            'original_amount': amount,
            'account_id': 1,
            'currency_id': usd_currency_id,
            'amount': Decimal(str(new_amount)),
            'type': 'credit',
            'fx_rate': 0.053,
        }
    )
