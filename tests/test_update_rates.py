import copy

from src.handlers.update_rates import CURRENCIES, update_rates


def test_update_mxn_to_usd_rates():
    tmp_currencies = copy.deepcopy(CURRENCIES)
    new_rates = {
        'MXN': {
            'USD': 0.02
        },
    }
    update_rates(new_rates, currencies=tmp_currencies)

    assert tmp_currencies['MXN']['USD'] == 0.02
    assert tmp_currencies['USD']['MXN'] == 18.70


def test_update_usd_to_mxn_rates():
    tmp_currencies = copy.deepcopy(CURRENCIES)

    new_rates = {
        'USD': {
            'MXN': 19.99
        }
    }
    update_rates(new_rates, currencies=tmp_currencies)

    assert tmp_currencies['USD']['MXN'] == 19.99
    assert tmp_currencies['MXN']['USD'] == 0.053


def test_update_not_valid_rate():
    tmp_currencies = copy.deepcopy(CURRENCIES)

    new_rates = {
        'MXN': {
            'JPY': 7.88
        },
        'JPY': {
            'MXN': 0.13
        }
    }

    update_rates(new_rates, currencies=tmp_currencies)

    assert tmp_currencies == CURRENCIES
