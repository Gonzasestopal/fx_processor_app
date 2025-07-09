# Payment FX Processor

This repo contains transactions processing functionality.

![Architecture](architecture.png)

## Table of Contents
- [Assumptions](#assumptions)
- [Requirements](#requirements)
- [Tests](#tests)
- [Entities](#entities)

## Assumptions

- Wallets will be created upon funding.
- Wallets will be unique by user_id and currency.

## Requirements

Python >= 3.11

## Tests

Make sure everything is running as expected by running our tests

```sh
pytest
```

## Entities

We consider users as our customers, who can own multiple wallets. These wallets store updated balance considering every transaction, thus a wallet will have many transactions associated. Both wallets and transaction will have a currency associated.

![Entities](entities.png)
