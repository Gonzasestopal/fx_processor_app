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
    storage.find.return_value = []
    user_id = 1
    response = view_balances(user_id, storage)
    assert isinstance(response, dict)
