from pydantic import BaseModel
from datetime import date, datetime, time, timedelta


class CreateKnowledgeRequest(BaseModel):
    planned_start: datetime = None
    user_email: str


class UpdateKnowledgeRequest(BaseModel):
    id: int
    planned_start: datetime = None
    user_email: str = None
