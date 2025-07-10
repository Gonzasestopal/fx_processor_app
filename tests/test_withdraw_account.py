from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from src.handlers.withdraw_account import withdraw_account


def test_not_sufficient_balance():
    storage = Mock()
    user_id = 1
    currency = 'MXN'
    amount = 100
    with pytest.raises(ValueError):
        withdraw_account(
            user_id,
            currency,
            amount,
            storage,
        )


def test_not_existing_account():
    storage = Mock()
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


def test_not_existing_currency():
    storage = Mock()
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
    withdraw_account(
        user_id,
        currency,
        amount,
        storage,
    )
    assert storage.assert_called_once()
