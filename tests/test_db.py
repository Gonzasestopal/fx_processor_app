import pytest

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


def test_insert_new_obj_id():
    Memory._instance = None

    account = Account(
        id=1,
        user_id=1,
        currency_id=1,
        amount=100,
    )

    memory = Memory(storage={'accounts': [account.model_dump()]})

    new_obj = memory.insert('accounts', {'user_id': 1, 'currency_id': '2', 'amount': 0})

    assert new_obj['id'] == 2


def test_insert_clash_unique():
    Memory._instance = None

    account = Account(
        id=1,
        user_id=1,
        currency_id=1,
        amount=100,
    )

    memory = Memory(storage={'accounts': [account.model_dump()]})

    with pytest.raises(Exception):
        memory.insert('accounts', {'user_id': 1, 'currency_id': '1', 'amount': 0})


def test_insert_new_obj_id_non_consecutive_records():
    Memory._instance = None

    account = Account(
        id=1,
        user_id=1,
        currency_id=1,
        amount=100,
    )

    another_account = Account(
        id=3,
        user_id=3,
        currency_id=1,
        amount=100,
    )

    memory = Memory(storage={'accounts': [account.model_dump(), another_account.model_dump()]})

    new_obj = memory.insert('accounts', {'user_id': 1, 'currency_id': '1', 'amount': 0})

    assert new_obj['id'] == 4


def test_find_one():
    Memory._instance = None

    memory = Memory()

    record = memory.find_one('currencies', id=1)

    assert record == {'id': 1, 'name': 'MXN'}


def test_find_one_by_key():
    Memory._instance = None

    memory = Memory()

    record = memory.find_one('currencies', name='MXN')

    assert record == {'id': 1, 'name': 'MXN'}


def test_find_one_not_found():
    Memory._instance = None

    memory = Memory()

    record = memory.find_one('currencies', name='JPN')

    assert record == None
