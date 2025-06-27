import logging
from typing import Iterable, List, cast, Generator, Iterator

from typing_extensions import Any

from sqlalchemy import select, text
from sqlalchemy import exc

from infrastructure.database.sql.api.engine import DBEngine, DBEngineAbstract
from infrastructure.database.sql.models.test_knowledge import TestKnowledge, \
    AssociationKnowledgeFlashCard
from infrastructure.database.sql.models.flash_card import FlashCard
from infrastructure.database.sql.api.exception.flash_card_exception import FlashCardHttpException
from infrastructure.routers.models.request.flash_card import \
    CreateFlashCardRequest

logger = logging.getLogger("root")


class CreateFlashCardDBAPI(DBEngineAbstract):

    def insert(
            self,
            flash_card_datas: List[CreateFlashCardRequest],
    ) -> Iterable[FlashCard]:
        """
        :param external_login_data:
        :param user_data:
        :return: list of id of created models
        """
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

    def _select_flash_card_from_id(self, id_flash_card: int):
        try:
            return select(FlashCard).where(
                cast(
                    "ColumnElement[bool]",
                    FlashCard.id == str(id_flash_card)
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

    def query_flash_card(
            self,
            flash_card_id: int,
            page: int = None
    ) -> Iterator[Any]:
        try:
            return next(
                self.query_statement(
                    self._select_flash_card_from_id(flash_card_id),
                    FlashCard,
                    page
                )
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select flash card {flash_card_id} -> {e}"
            )
            raise FlashCardHttpException(
                detail=f"Can not select flash card {flash_card_id}",
                status_code=400
            )

    def query_flash_cards_generator(
            self,
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                    self._select_all_flash_card_sql()
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