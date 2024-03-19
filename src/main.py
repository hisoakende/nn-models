from fastapi import FastAPI, status
from fastapi.responses import Response

from src.router import router

app = FastAPI(title='Models service')

app.include_router(router)


@app.get('/_health')
async def check_health() -> Response:
    return Response(status_code=status.HTTP_200_OK)
