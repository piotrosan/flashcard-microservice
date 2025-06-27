from pydantic import BaseModel


class CreateFlashCardRequest(BaseModel):
    word: str
    translate: str