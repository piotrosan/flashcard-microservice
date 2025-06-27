import os


root_path = os.path.abspath(os.path.dirname(__file__))

# APP CONFIG
APP_ID = '216d9d8c-3a23-11f0-8bd8-0800270ff509'
NAME = 'Flash Card'
NA_ME = 'flash-dard'

SSL_KEYFILE = None
SSL_CERTFILE = None
DOMAIN = 'localhost'
PORT = 8002

BASE_URL = f"{'https' if SSL_CERTFILE else 'http'}://{DOMAIN}:{PORT}"

# database
PAGINATION_PER_PAGE = 50

POSTGRES_HOST_WITH_PORT = "localhost:5432"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "example"
DATABASE_NAME = "flash_card"

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST_WITH_PORT}/{DATABASE_NAME}"

# "postgresql+psycopg2://postgres:example@localhost:5432/flash_card"

