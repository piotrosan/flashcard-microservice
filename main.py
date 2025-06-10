import uvicorn
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from infrastructure.security.middleware.auth import TokenAuthBackend
from infrastructure.routers import flash_card, user_permission
from settings import DOMAIN, PORT

# middlewares = [
#     Middleware(AuthenticationMiddleware, backend=TokenAuthBackend()),
# ]
#
# app = FastAPI(middleware=middlewares)

app = FastAPI()
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