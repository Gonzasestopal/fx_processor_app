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
    )

    print(tx)

    assert tx.original_amount == 100
    assert tx.original_currency_id == 1

