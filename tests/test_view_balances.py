from decimal import Decimal
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from src.handlers.view_balances import view_balances


def test_account_not_found():
    storage = Mock()
    storage.find.return_value = []
    user_id = 1
    with pytest.raises(HTTPException):
        view_balances(user_id)


def test_return_value():
    storage = Mock()
    storage.find.return_value = [
        {'id': 1, 'user_id': 1, 'currency_id': 1, 'amount': 100},
        {'id': 2, 'user_id': 1, 'currency_id': 2, 'amount': 25},
    ]
    storage.find_one.side_effect = [{'id': 1, 'name': 'MXN'}, {'id': 2, 'name': 'USD'}]
    user_id = 1
    response = view_balances(user_id, storage)
    assert isinstance(response, dict)


def test_decimal_conversions():
    storage = Mock()
    storage.find.return_value = [
        {'id': 1, 'user_id': 1, 'currency_id': 1, 'amount': Decimal('13.01')},
        {'id': 2, 'user_id': 1, 'currency_id': 2, 'amount': Decimal('9.99')},
    ]
    storage.find_one.side_effect = [{'id': 1, 'name': 'MXN'}, {'id': 2, 'name': 'USD'}]
    user_id = 1
    response = view_balances(user_id, storage)

    assert response == {
        'MXN': 13,
        'USD': 10,
    }
