import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def login(request: Request, call_next):

    response = await call_next(request)
    return response