import logging
from typing import Sequence, Iterable, List, cast
from uuid import UUID

from typing_extensions import Any

from sqlalchemy import Select, Update, select, Row, and_, text, String
from sqlalchemy import exc

from .engine import BEngine
from ..sql.models.flash_card import FlashCard
from ..sql.models.test_knowledge import TestKnowledge, \
    AssociationKnowledgeFlashCard
from ...exception.flash_card_exception import FlashCardHttpException

logger = logging.getLogger("root")


class FlashCardDBAPI(BEngine):

    def insert_test_knowledge_with_flash_card(
            self,
            flash_card_data: dict,
            test_knoledge_data: dict
    ) -> Iterable[TestKnowledge]:
        """
        :param external_login_data:
        :param user_data:
        :return: list of id of created models
        """
        try:
            flash_card = FlashCard(**flash_card_data)
            test_knowledge = TestKnowledge(**test_knoledge_data)
            test_knowledge.flash_cards = [
                AssociationKnowledgeFlashCard(flash_card=flash_card)
            ]
            return self.insert_objects([test_knowledge])
        except exc.SQLAlchemyError as e:
            logger.critical(f"Problem wile insert user {flash_card} -> {e}")
            raise FlashCardHttpException(
                detail="Can not insert flash card",
                status_code=400
            )

    def _select_all_flash_card(
            self,
            column: List[str] = None,
            order: List[str] = None
    ):
        tmp_select = select(FlashCard)

        if column:
            tmp_select.column(*[text(col) for col in column])

        tmp_select.join_from(
            TestKnowledge,
            FlashCard
        )
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

    def _select_all_flash_card_from_test_knowledge(self, id_knowledge: int):
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
            order: List[str] = None
    ) -> Row[Any]:
        try:
            return self.query_statement(
                self._select_all_flash_card(column, order)
            )
        except exc.SQLAlchemyError as e:
            logger.critical("Problem wile select all flasgh")
            raise FlashCardHttpException(
                detail="Can not select flash cards with attchments",
                status_code=400
            )

    def query_flash_card_generator(
            self,
            flash_card_id: int
    ) -> Row[Any]:
        try:
            return self.query_statement(
                self._select_flash_card_from_id(flash_card_id)
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select flash card {flash_card_id} -> {e}"
            )
            raise FlashCardHttpException(
                detail=f"Can not select flash card {flash_card_id}",
                status_code=400
            )

    def raw_query_flash_card(
            self,
            select_query: Select[Any],
    ) -> Sequence[Row]:
        try:
            return list(self.query_statement(select_query))
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select flash card from "
                f"custom select statement -> {e}"
            )
            raise FlashCardHttpException(
                detail="Can not select flash card",
                status_code=400
            )

    def raw_query_user_generator(
            self,
            select_query: Select[Any],
    ) -> Row[Any]:
        try:
            return self._query_statement(
                self.query_statement(select_query)
            ).all()
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select user from "
                f"custom select statement -> {e}"
            )
            raise HttpUserDBException(
                detail="Can not select user",
                status_code=400
            )

    def get_all_context_for_user(
            self,
            user_hash: UUID
    ) -> Row[Any]:
        try:
            return self.query_statement(
                self._select_all_data_user_from_hash(user_hash)
            )
        except exc.SQLAlchemyError as e:
            logger.critical("Problem wile select all users")
            raise HttpUserDBException(
                detail=f"Can not select user {e}",
                status_code=400
            )