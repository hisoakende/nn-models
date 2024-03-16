from fastapi import FastAPI

from src.router import router

app = FastAPI(title='Models service')

app.include_router(router)
