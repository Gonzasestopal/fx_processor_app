MXN_CONVERSION_RATES = {
    'USD': 0.053
}

USD_CONVERSION_RATES = {
    'MXN': 18.70
}

CURRENCIES = {
    'MXN': MXN_CONVERSION_RATES,
    'USD': USD_CONVERSION_RATES,
}


def update_rates(new_rates, currencies=CURRENCIES):
    if currencies is None:
        currencies = CURRENCIES

    for rate, converted_rates in new_rates.items():
        if rate not in currencies:
            continue

        for converted_rate, amount in converted_rates.items():
            if converted_rate not in currencies[rate]:
                continue
            currencies[rate][converted_rate] = amount
