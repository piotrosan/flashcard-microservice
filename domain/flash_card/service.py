from typing import List, Iterable, Tuple

from infrastructure.database.sql.api.flash_card_database_api import FlashCardDBAPI
from infrastructure.database.sql.models import FlashCard
from infrastructure.database.sql.models.flash_card import Language
from infrastructure.routers.models.request.flash_card import \
    CreateFlashCardRequest, CreateLanguageRequest


class FashCardService:

    def __init__(self, infrastructure_db: FlashCardDBAPI):
        self.infrastructure_db = infrastructure_db

    def list_flash_cards(self):
        return self.infrastructure_db.query_flash_cards_generator()

    def get_random_flash_card(self):
        pass

    def get_flash_card(self, flash_card: int):
        pass

    def create_flash_card(
            self,
            flash_card_datas: List[CreateFlashCardRequest]
    )-> Iterable[FlashCard]:
        return self.infrastructure_db.insert(flash_card_datas)

    def create_language(
            self,
            languages: List[CreateLanguageRequest]
    )-> Iterable[Language]:
        return self.infrastructure_db.insert_languages(languages)

    def get_language(
            self,
            page_id: int = None
    )-> Iterable[Tuple[Language]]:
        return self.infrastructure_db.query_languages(page_id)
