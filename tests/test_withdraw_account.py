from unittest.mock import Mock

from src.handlers.withdraw_account import withdraw_account


def test_not_sufficient_balance():
    storage = Mock()
    user_id = 1
    currency = 'MXN'
    amount = 100
    response = withdraw_account(
        user_id,
        currency,
        amount,
        storage,
    )
    assert response == True


def test_not_existing_account():
    storage = Mock()
    user_id = 1
    currency = 'MXN'
    amount = 100
    response = withdraw_account(
        user_id,
        currency,
        amount,
        storage,
    )
    assert response == True


def test_not_existing_currency():
    storage = Mock()
    user_id = 1
    currency = 'MXN'
    amount = 100
    response = withdraw_account(
        user_id,
        currency,
        amount,
        storage,
    )
    assert response == True


def test_new_updated_balance():
    storage = Mock()
    user_id = 1
    currency = 'MXN'
    amount = 100
    response = withdraw_account(
        user_id,
        currency,
        amount,
        storage,
    )
    assert response == True
