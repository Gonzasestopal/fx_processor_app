from unittest.mock import Mock

from expects import be, equal, expect, have_keys, raise_error
from fastapi import HTTPException
from mamba import before, context, description, it

from src.handlers.fund_account import fund_account

with description(fund_account) as self:
    with before.each:
        self.storage = Mock()

    with before.all:
        self.user_id = 1
        self.currency = 'MXN'
        self.amount = 100

    with context('currency is not found'):
        with it('raises exception'):
            self.storage.find_one.return_value = None

            expect(lambda: fund_account(
                self.user_id,
                self.currency,
                self.amount,
                self.storage,
            )).to(raise_error(HTTPException))

    with context('account is not found'):
        with it('creates account and inserts fund transaction'):
            self.storage.find_one.side_effect = [{'id': 1, 'name': 'MXN'}, None]
            self.storage.insert.return_value = {
                'id': 1,
                'user_id': 1,
                'currency_id': 1,
                'amount': 0,
            }

            fund_account(
                self.user_id,
                self.currency,
                self.amount,
                self.storage,
            )

            expect(self.storage.insert.call_count).to(be(2))

    with it('updates existing account and inserts fund transaction'):
        self.storage.find_one.side_effect = [{'id': 1, 'name': 'MXN'}, {
            'id': 1,
            'user_id': 1,
            'currency_id': 1,
            'amount': 50,
        }]

        fund_account(
            self.user_id,
            self.currency,
            self.amount,
            self.storage,
        )

        (args,), kwargs = self.storage.update.call_args

        expect(args).to(equal('accounts'))
        expect(kwargs['filters']).to(have_keys({
            'user_id': self.user_id,
            'currency_id': 1,
        }))
        expect(kwargs['new_values']).to(have_keys({
            'amount': self.amount + 50
        }))
