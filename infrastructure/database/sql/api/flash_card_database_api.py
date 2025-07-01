import logging
from typing import Iterable, List, cast, Iterator

from typing_extensions import Any

from sqlalchemy import select, text
from sqlalchemy import exc

from infrastructure.database.sql.api.engine import DBEngine, DBEngineAbstract
from infrastructure.database.sql.models.test_knowledge import TestKnowledge

from infrastructure.database.sql.models.flash_card import FlashCard, Language
from infrastructure.database.sql.api.exception.flash_card_exception import FlashCardHttpException
from infrastructure.routers.models.request.flash_card import (
    CreateFlashCardRequest,
    CreateLanguageRequest
)


logger = logging.getLogger("root")


class CreateFlashCardDBAPI(DBEngineAbstract):

    def insert(
            self,
            flash_card_datas: List[CreateFlashCardRequest],
    ) -> Iterable[FlashCard]:
        try:

            return self.insert_objects([
                FlashCard(**fcd.model_dump(mode='python'))
                for fcd in flash_card_datas
            ])
        except exc.SQLAlchemyError as e:
            logger.critical(f"Problem wile insert flash card -> {e}")
            raise FlashCardHttpException(
                detail="Can not insert flash card",
                status_code=400
            )

    def insert_languages(
            self,
            languages: List[CreateLanguageRequest],
    ) -> Iterable[Language]:
        try:

            return self.insert_objects([
                Language(**l.model_dump(mode='python'))
                for l in languages
            ])
        except exc.SQLAlchemyError as e:
            logger.critical(f"Problem wile insert language -> {e}")
            raise FlashCardHttpException(
                detail="Can not insert language",
                status_code=400
            )


class GetFlashCardDBAPI(DBEngineAbstract):

    def _select_all_flash_card_sql(
            self,
            column: List[str] = None,
            order: List[str] = None
    ):
        tmp_select = select(FlashCard)

        if column:
            tmp_select.column(*[text(col) for col in column])

        if order:
            tmp_select.order_by(*[text(col) for col in order])

        return tmp_select

    def _select_flash_card_from_id(self, ids_flash_card: List[int]):
        try:
            return select(FlashCard).where(
                cast(
                    "ColumnElement[bool]",
                    FlashCard.id.in_(ids_flash_card)
                )
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select flash card from id {e}")
            raise FlashCardHttpException(
                detail="Can not select flash card",
                status_code=400
            )

    def _select_all_flash_card_with_test_knowledge_for_test(
            self,
            id_knowledge: int
    ):
        try:
            return select(FlashCard, TestKnowledge).where(
                cast(
                    "ColumnElement[bool]",
                    TestKnowledge.id == str(id_knowledge)
                )
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select flash card from test knowledge id {e}")
            raise FlashCardHttpException(
                detail="Can not select flash cards",
                status_code=400
            )

    def _select_languages(self):
        try:
            return select(Language)
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select Language dictionary {e}")
            raise FlashCardHttpException(
                detail="Can not select Language",
                status_code=400
            )

    def query_languages(
            self,
            page: int = None
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                    self._select_languages(),
                    Language,
                    page
                )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select languages -> {e}"
            )
            raise FlashCardHttpException(
                detail=f"Can not select languages",
                status_code=400
            )


    def query_all_flash_card_with_attachments_generator(
            self,
            column: List[str] = None,
            order: List[str] = None,
            page: int = None
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                self._select_all_flash_card_sql(column, order),
                FlashCard,
                page
            )
        except exc.SQLAlchemyError as e:
            logger.critical("Problem wile select all flasgh")
            raise FlashCardHttpException(
                detail="Can not select flash cards with attchments",
                status_code=400
            )

    def query_flash_cards(
            self,
            flash_card_ids: List[int],
            page: int = None
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                    self._select_flash_card_from_id(flash_card_ids),
                    FlashCard,
                    page
                )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select flash card {flash_card_ids} -> {e}"
            )
            raise FlashCardHttpException(
                detail=f"Can not select flash card {flash_card_ids}",
                status_code=400
            )

    def query_flash_cards_generator(
            self,
            page_id: int
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                    self._select_all_flash_card_sql(),
                    FlashCard,
                    page_id
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select flash cards -> {e}"
            )
            raise FlashCardHttpException(
                detail=f"Can not select flash cards",
                status_code=400
            )


class UpdateFlashCardDBAPI(DBEngineAbstract):
    pass


class FlashCardDBAPI(
    CreateFlashCardDBAPI,
    GetFlashCardDBAPI,
    UpdateFlashCardDBAPI,
    DBEngine
):
    pass