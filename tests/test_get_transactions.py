from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from src.handlers.get_transactions import get_transactions
from src.models import Account, Transaction


def test_account_not_found():
    user_id = 1
    with pytest.raises(HTTPException):
        get_transactions(user_id)


def test_transactions_return_value():
    user_id = 1

    transaction = Transaction(
        id=1,
        type='debit',
        account_id=1,
        currency_id=1,
        amount=100,
    )

    another_transaction = Transaction(
        id=2,
        type='credit',
        account_id=1,
        currency_id=1,
        amount=50,
    )

    different_account_transaction = Transaction(
        id=3,
        type='debit',
        account_id=2,
        currency_id=1,
        amount=100,
    )

    account = Account(
        id=1,
        user_id=1,
        amount=100,
        currency_id=1,
    )

    storage = Mock()
    storage.find_one.return_value = account.model_dump()
    storage.find.return_value = [
        transaction.model_dump(),
        another_transaction.model_dump(),
        different_account_transaction.model_dump(),
    ]

    transactions = get_transactions(user_id, storage=storage)

    assert transaction.model_dump() in transactions
    assert another_transaction.model_dump() in transactions
    assert different_account_transaction.model_dump() in transactions
