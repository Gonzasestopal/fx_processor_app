
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from src.handlers.convert_currency import convert_currency


def test_convert_currency_mxn():
    user_id = 1
    currency = 'MXN'
    new_currency = 'USD'
    amount = 100
    storage = Mock()
    account = {'amount': 100}

    mxn_currency = {'id': 1, 'name': 'MXN'}
    usd_currency = {'id': 2, 'name': 'USD'}
    storage.find_one.side_effect = [mxn_currency, usd_currency, account]

    result = convert_currency(user_id, currency, new_currency, amount, storage)

    assert result == (amount * 0.053)


def test_convert_currency_usd():
    user_id = 1
    currency = 'USD'
    new_currency = 'MXN'
    amount = 100
    storage = Mock()
    account = {'amount': 100}

    mxn_currency = {'id': 1, 'name': 'MXN'}
    usd_currency = {'id': 2, 'name': 'USD'}
    storage.find_one.side_effect = [usd_currency, mxn_currency, account]

    result = convert_currency(user_id, currency, new_currency, amount, storage)

    assert result == (amount * 18.70)


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
    assert True


def test_new_account_not_exist():
    assert True


def test_new_account_balance():
    assert True
