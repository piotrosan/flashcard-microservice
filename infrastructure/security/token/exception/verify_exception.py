from fastapi import HTTPException


class TokenExpired(HTTPException):
    pass


class TokenDifferentAppId(HTTPException):
    pass