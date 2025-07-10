
from src.handlers.convert_currency import convert_currency


def test_convert_currency_mxn():
    user_id = 1
    currency = 'MXN'
    new_currency = 'USD'
    amount = 100

    result = convert_currency(user_id, currency, new_currency, amount)

    assert result == True


def test_convert_currency_usd():
    user_id = 1
    currency = 'USD'
    new_currency = 'MXN'
    amount = 100

    result = convert_currency(user_id, currency, new_currency, amount)

    assert result == True


def test_currency_not_found():
    user_id = 1
    currency = 'USD'
    new_currency = 'MXN'
    amount = 100

    result = convert_currency(user_id, currency, new_currency, amount)

    assert result == True


def test_new_currency_not_found():
    user_id = 1
    currency = 'USD'
    new_currency = 'MXN'
    amount = 100

    result = convert_currency(user_id, currency, new_currency, amount)

    assert result == True


def test_insufficient_balance():
    user_id = 1
    currency = 'USD'
    new_currency = 'MXN'
    amount = 100

    result = convert_currency(user_id, currency, new_currency, amount)

    assert result == True


def test_account_not_found():
    user_id = 1
    currency = 'USD'
    new_currency = 'MXN'
    amount = 100

    result = convert_currency(user_id, currency, new_currency, amount)

    assert result == True
