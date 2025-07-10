from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from src.handlers.withdraw_account import withdraw_account


def test_not_sufficient_balance():
    storage = Mock()
    storage.find_one.side_effect = [
        {'id': 1, 'name': 'MXN'},
        {'id': 1, 'user_id': 1, 'currency_id': 1, 'amount': 99}
    ]
    user_id = 1
    currency = 'MXN'
    amount = 100
    with pytest.raises(HTTPException) as exc_info:
        withdraw_account(
            user_id,
            currency,
            amount,
            storage,
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Insufficient Balance"


def test_not_existing_account():
    storage = Mock()
    user_id = 1
    currency = 'MXN'
    amount = 100
    storage.find_one.side_effect = [{'id': 1, 'name': 'MXN'}, None]

    with pytest.raises(HTTPException):
        withdraw_account(
            user_id,
            currency,
            amount,
            storage,
        )


def test_not_existing_currency():
    storage = Mock()
    storage.find_one.return_value = None
    user_id = 1
    currency = 'MXN'
    amount = 100
    with pytest.raises(HTTPException):
        withdraw_account(
            user_id,
            currency,
            amount,
            storage,
        )


def test_new_updated_balance():
    storage = Mock()
    user_id = 1
    currency = 'MXN'
    amount = 100
    account = {'id': 1, 'user_id': 1, 'currency_id': 1, 'amount': 101}
    currency_obj = {'id': 1, 'name': 'MXN'}
    storage.find_one.side_effect = [
        currency_obj,
        account,
    ]
    user_id = 1
    currency = 'MXN'
    amount = 100
    withdraw_account(
        user_id,
        currency,
        amount,
        storage,
    )
    storage.update.assert_called_once_with(
        'accounts',
        filters={'user_id': user_id, 'currency_id': currency_obj['id']},
        new_values={'amount': account['amount'] - amount}
    )
