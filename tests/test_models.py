from datetime import datetime
from decimal import Decimal

from src.models import Transaction


def test_transaction():
    tx = Transaction(
        id=1,
        amount=100,
        type='debit',
        account_id=1,
        currency_id=1,
    )

    assert tx.amount == 100
    assert tx.id == 1
    assert tx.type == 'debit'
    assert tx.account_id == 1
    assert tx.currency_id == 1


def test_transaction_with_default_values():
    tx = Transaction(
        id=1,
        amount=100,
        type='debit',
        account_id=1,
        currency_id=1,
        fx_rate=0.0053
    )

    assert tx.original_amount == 100
    assert tx.original_currency_id == 1
    assert tx.fx_rate == 0.0053


def test_transaction_with_decimal_to_int_values():
    tx = Transaction(
        id=1,
        amount=Decimal('0.03'),
        type='debit',
        original_amount=Decimal('9.99'),
        account_id=1,
        currency_id=1,
        fx_rate=0.0053,
    )

    assert tx.amount == 0
    assert tx.original_amount == 10


def test_transaction_with_conversion_auditing_values():
    tx = Transaction(
        id=1,
        amount=100,
        type='debit',
        account_id=1,
        currency_id=1,
        fx_rate=0.0053,
        conversion_id='uuid',
        created_at='2024-04-09',
    )

    assert tx.created_at == datetime.fromisoformat('2024-04-09')
    assert tx.conversion_id == 'uuid'
