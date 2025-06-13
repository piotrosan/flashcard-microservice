from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from infrastructure.security.middleware.auth import TokenAuthBackend
from infrastructure.routers import flash_card, user_permission
from settings import DOMAIN, PORT
from infrastructure.webhooks.register import AppRegister

# middlewares = [
#     Middleware(AuthenticationMiddleware, backend=TokenAuthBackend()),
# ]
#
# app = FastAPI(middleware=middlewares)

def register_app():
    ar = AppRegister()
    ar.send_register_request()

def unregister_app():
    ar = AppRegister()
    ar.send_unregister_request()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Register app in cache
    register_app()
    yield
    # Unregistered while restart
    unregister_app()



app = FastAPI(lifespan=lifespan)
# include
app.include_router(flash_card.router)
app.include_router(user_permission.router)


@app.get("/")
async def root():
    return {"message": "Ping"}


if __name__ == "__main__":
    # Start uvicorn
    # https://stackoverflow.com/questions/69207474/enable-https-using-uvicorn
    uvicorn.run(
        app,
        host=DOMAIN,
        port=PORT
    )