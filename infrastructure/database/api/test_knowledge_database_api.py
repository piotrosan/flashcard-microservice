import logging
from typing import Iterable, List, cast

from typing_extensions import Any

from sqlalchemy import select, Row, text
from sqlalchemy import exc

from infrastructure.database.api.engine import DBEngine, DBEngineAbstract
from infrastructure.database.sql.models.test_knowledge import TestKnowledge
from infrastructure.database.sql.models.flash_card import FlashCard
from infrastructure.exception.test_knowledge_exception import TestKnowledgeHttpException

logger = logging.getLogger("root")


class CreateTestKnowledgeDBAPI(DBEngineAbstract):

    def insert(
            self,
            test_knoledge_data: dict
    ) -> Iterable[TestKnowledge]:
        """
        :param external_login_data:
        :param user_data:
        :return: list of id of created models
        """
        try:
            test_knowledge = TestKnowledge(**test_knoledge_data)
            return self.insert_objects([test_knowledge])
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile insert test "
                f"knowledge {test_knoledge_data} -> {e}"
            )
            raise TestKnowledgeHttpException(
                detail="Can not insert test knowledge",
                status_code=400
            )


class GetTestKnowledgeDBAPI(DBEngineAbstract):

    def _select_all_test_knowledge_sql(
            self,
            column: List[str] = None,
            order: List[str] = None
    ):
        tmp_select = select(TestKnowledge)

        if column:
            tmp_select.column(*[text(col) for col in column])

        if order:
            tmp_select.order_by(*[text(col) for col in order])

        return tmp_select


    def _select_test_knowledge_from_id_sql(self, id_test_knowledge: int):
        try:
            return select(TestKnowledge).where(
                cast(
                    "ColumnElement[bool]",
                    TestKnowledge.id == str(id_test_knowledge)
                )
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select flash card from id {e}")
            raise TestKnowledgeHttpException(
                detail="Can not create select test knowledge",
                status_code=400
            )

    def _select_test_knowledge_with_all_flash_cards_sql(
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
            raise TestKnowledgeHttpException(
                detail="Can not create select test knowledge",
                status_code=400
            )

    def query_all_test_knowledge_generator(
            self,
            column: List[str] = None,
            order: List[str] = None
    ) -> Row[Any]:
        try:
            return self.query_statement(
                self._select_all_test_knowledge_sql(column, order)
            )
        except exc.SQLAlchemyError as e:
            logger.critical("Problem wile select all test knowledge")
            raise TestKnowledgeHttpException(
                detail="Can not select test knowledge",
                status_code=400
            )

    def query_test_knowledge_with_flash_cards(
            self,
            id_knowledge: int
    ) -> Row[Any]:
        try:
            return self.query_statement(
                self._select_test_knowledge_with_all_flash_cards_sql(
                    id_knowledge
                )
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select test knowledge {id_knowledge} -> {e}"
            )
            raise TestKnowledgeHttpException(
                detail=f"Can not select test knowledge {id_knowledge}",
                status_code=400
            )

    def query_test_knowledge_from_id(
            self,
            id_knowledge: int
    ) -> Row[Any]:
        try:
            return self.query_statement(
                self._select_test_knowledge_from_id_sql(id_knowledge)
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select test knowledge {id_knowledge} -> {e}"
            )
            raise TestKnowledgeHttpException(
                detail=f"Can not select test knowledge {id_knowledge}",
                status_code=400
            )


class UpdateKnowledgeDBAPI(DBEngineAbstract):
    pass


class TestKnowledgeDBAPI(
    CreateTestKnowledgeDBAPI,
    GetTestKnowledgeDBAPI,
    UpdateKnowledgeDBAPI,
    DBEngine
):
    pass