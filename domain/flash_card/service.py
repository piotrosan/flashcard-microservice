from typing import List, Iterable, Tuple, Any, Iterator

from infrastructure.database.sql.api.flash_card_database_api import FlashCardDBAPI
from infrastructure.database.sql.models import FlashCard
from infrastructure.database.sql.models.flash_card import Language
from infrastructure.routers.models.request.flash_card import \
    CreateFlashCardRequest, CreateLanguageRequest
from infrastructure.supporter.generic import random_from


class FashCardService:

    def __init__(self, infrastructure_db: FlashCardDBAPI):
        self.infrastructure_db = infrastructure_db

    def get_flash_cards(self, page_id: int) -> Iterator[Any]:
        return self.infrastructure_db.query_flash_cards_generator(page_id)

    def get_flash_cards_from_ids_list(self, flash_cards: List[int]) -> Iterator[Any]:
        return self.infrastructure_db.query_flash_cards(flash_cards)

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
