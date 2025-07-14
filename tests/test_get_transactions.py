from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from src.handlers.get_transactions import get_transactions


def test_account_not_found():
    user_id = 1
    with pytest.raises(HTTPException):
        get_transactions(user_id)


def test_transactions_return_value():
    user_id = 1
    transactions = get_transactions(user_id)

    assert isinstance(transactions, list)
