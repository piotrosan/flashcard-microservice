from typing import List

from pydantic import BaseModel


class CreateFlashCardRequest(BaseModel):
    word: str
    translate: List[str]
    language_id: int

class CreateLanguageRequest(BaseModel):
    shortcut: str
    full_name: str