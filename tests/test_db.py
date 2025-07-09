from src.db import Memory
from src.models import Account


def test_storage_defaults():
    memory = Memory()

    assert memory.storage == {
        'currencies': [
            {'id': 1, 'name': 'MXN'},
            {'id': 2, 'name': 'USD'},
        ],
    }


def test_missing_get_table():
    Memory._instance = None

    memory = Memory(storage={})

    assert memory.get_table('accounts') == []


def test_get_table():
    account = Account(
        id=1,
        user_id=1,
        currency_id=1,
        amount=100,
    )
    storage = {
        'accounts': [account.model_dump()]
    }
    Memory._instance = None

    memory = Memory(storage=storage)

    assert memory.get_table('accounts') == [account.model_dump()]


def test_insert():
    Memory._instance = None

    account = Account(
        id=1,
        user_id=1,
        currency_id=1,
        amount=100,
    )

    memory = Memory(storage={})

    memory.insert('accounts', account.model_dump())

    assert memory.get_table('accounts') == [account.model_dump()]
