from src.router import router

from fastapi import FastAPI

app = FastAPI(title='Models service')

app.include_router(router)
