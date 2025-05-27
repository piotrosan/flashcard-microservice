from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from infrastructure.security.middleware.auth import TokenAuthBackend
from infrastructure.routers import flash_card

middlewares = [
    Middleware(AuthenticationMiddleware, backends=TokenAuthBackend()),
]

app = FastAPI(middleware=middlewares)

# include
app.include_router(flash_card.router)


@app.get("/")
async def root():
    return {"message": "Ping"}