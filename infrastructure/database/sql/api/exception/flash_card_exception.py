from fastapi import HTTPException


class FlashCardHttpException(HTTPException):
    status_code = 400
    detail = "Problem with work on flash card"