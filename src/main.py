
import random
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_utilities import repeat_at

from src.handlers.update_rates import update_rates
from src.routes import accounts


@asynccontextmanager
async def lifespan(app: FastAPI):
    retrieve_new_fx()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(accounts.router, prefix='/wallets', tags=['Accounts'])


@repeat_at(cron="* * * * *")
def retrieve_new_fx():

    new_rates = {
        'MXN': {
            'USD': random_float_0_05_0_06()
        },
        'USD': {
            'MXN': random_float_18_20()
        }
    }

    update_rates(new_rates=new_rates)
    print(new_rates)


def random_float_18_20():
    return round(random.uniform(18, 20), 2)


def random_float_0_05_0_06():
    rand_int = random.randint(50, 60)
    return rand_int / 1000
