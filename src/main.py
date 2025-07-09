
from fastapi import FastAPI

from src.routes import accounts

app = FastAPI()

app.include_router(accounts.router, prefix='/wallets', tags=['Accounts'])
