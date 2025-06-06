import os

APP_ID = '216d9d8c-3a23-11f0-8bd8-0800270ff509'
PAGINATION_PER_PAGE = 50


root_path = os.path.abspath(os.path.dirname(__file__))

SSL_KEYFILE = None
SSL_CERTFILE = None
DOMAIN = 'localhost'
PORT = 8002

BASE_URL = f"{'https' if SSL_CERTFILE else 'http'}://{DOMAIN}:{PORT}"