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
