from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from src.handlers.fund_account import fund_account


def test_no_currency_found():
    storage = Mock()
    user_id = 1
    currency = 'MXN'
    amount = 100

    storage.find_one.return_value = None
    with pytest.raises(HTTPException):
        fund_account(
            storage=storage,
            user_id=user_id,
            amount=amount,
            currency=currency,
        )


def test_no_account_found():
    storage = Mock()
    user_id = 1
    currency = 'MXN'
    amount = 100

    storage.insert.return_value = {'id': 1, 'user_id': 1, 'currency_id': 1, 'amount': 100}
    storage.find_one.side_effect = [{'id': 1, 'name': 'MXN'}, None]
    fund_account(
        storage=storage,
        user_id=user_id,
        amount=amount,
        currency=currency,
    )

    first_call_args, first_call_kwargs = storage.insert.call_args_list[0]

    assert first_call_args == ('accounts', {'amount': amount, 'user_id': user_id, 'currency_id': 1})


def test_fund_account():
    storage = Mock()
    user_id = 1
    currency = 'MXN'
    amount = 100

    storage.find_one.side_effect = [
        {'id': 1, 'name': 'MXN'},
        {'id': 1, 'user_id': 1, 'currency_id': 1, 'amount': 100},
    ]

    fund_account(
        storage=storage,
        user_id=user_id,
        amount=amount,
        currency=currency,
    )

    storage.update.assert_called_once_with(
        'accounts',
        filters={'user_id': 1, 'currency_id': 1},
        new_values={'amount': 200}
    )


def test_fund_account_return_value():
    storage = Mock()
    user_id = 1
    currency = 'MXN'
    amount = 100

    storage.insert.return_value = {'id': 1, 'user_id': 1, 'currency_id': 1, 'amount': 100}
    storage.find_one.side_effect = [
        {'id': 1, 'name': 'MXN'},
        {'id': 1, 'user_id': 1, 'currency_id': 1, 'amount': 100},
    ]

    account = fund_account(
        storage=storage,
        user_id=user_id,
        amount=amount,
        currency=currency,
    )

    assert account == storage.update.return_value


def test_fund_new_account_return_value():
    storage = Mock()
    user_id = 1
    currency = 'MXN'
    amount = 100

    storage.insert.return_value = {'id': 1, 'user_id': 1, 'currency_id': 1, 'amount': 100}
    storage.find_one.side_effect = [{'id': 1, 'name': 'MXN'}, None]

    account = fund_account(
        storage=storage,
        user_id=user_id,
        amount=amount,
        currency=currency,
    )

    assert account == storage.insert.return_value


def test_new_transaction():
    storage = Mock()
    user_id = 1
    currency = 'MXN'
    amount = 100
    storage.insert.return_value = {'id': 1, 'user_id': 1, 'currency_id': 1, 'amount': 100}
    storage.find_one.side_effect = [
        {'id': 1, 'name': 'MXN'},
        {'id': 1, 'user_id': 1, 'currency_id': 1, 'amount': 100},
    ]

    fund_account(
        storage=storage,
        user_id=user_id,
        amount=amount,
        currency=currency,
    )

    storage.insert.assert_called_once_with(
        'transactions',
        {
            'currency_id': 1,
            'account_id': 1,
            'amount': 100,
            'type': 'credit',
        }
    )


def test_new_transaction_new_account():
    storage = Mock()
    user_id = 1
    currency = 'MXN'
    amount = 100

    storage.insert.return_value = {'id': 1, 'user_id': 1, 'currency_id': 1, 'amount': 100}
    storage.find_one.side_effect = [
        {'id': 1, 'name': 'MXN'},
        None,
    ]

    fund_account(
        storage=storage,
        user_id=user_id,
        amount=amount,
        currency=currency,
    )

    second_call_args, second_call_kwargs = storage.insert.call_args_list[1]

    assert second_call_args == (
        'transactions',
        {
            'currency_id': 1,
            'account_id': 1,
            'amount': 100,
            'type': 'credit',
        }
    )
