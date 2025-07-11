from datetime import datetime

from infrastructure.routers.models.request.flash_card import \
    CreateFlashCardRequest, CreateLanguageRequest


class FlashCardResponse(CreateFlashCardRequest):
    id: int = None
    create_at: datetime = None
    updated_at: datetime | None = None


class LanguageResponse(CreateLanguageRequest):
    id: int = None
    create_at: datetime = None
    updated_at: datetime | None = None



