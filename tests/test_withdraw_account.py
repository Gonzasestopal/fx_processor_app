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
    storage.find_one.return_value = {'id': 1, 'name': 'MXN'}
    user_id = 1
    currency = 'MXN'
    amount = 100
    withdraw_account(
        user_id,
        currency,
        amount,
        storage,
    )
    assert storage.assert_called_once()
