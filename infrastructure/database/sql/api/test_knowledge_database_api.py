import logging
from typing import Iterable, List, cast, Generator

from typing_extensions import Any

from sqlalchemy import select, text, and_
from sqlalchemy import exc

from infrastructure.database.sql.api.analytics import AnalyticsSQLMixin
from infrastructure.database.sql.api.engine import DBEngine, DBEngineAbstract
from infrastructure.database.sql.models.test_knowledge import TestKnowledge
from infrastructure.database.sql.models.flash_card import FlashCard
from infrastructure.database.sql.api.exception.test_knowledge_exception import TestKnowledgeHttpException

logger = logging.getLogger("root")


class CreateTestKnowledgeDBAPIMixin(DBEngineAbstract):

    def insert(
            self,
            test_knowledge_data: dict
    ) -> Iterable[TestKnowledge]:
        try:
            test_knowledge = TestKnowledge(**test_knowledge_data)
            return self.insert_objects([test_knowledge])
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile insert test "
                f"knowledge {test_knowledge_data} -> {e}"
            )
            raise TestKnowledgeHttpException(
                detail="Can not insert test knowledge",
                status_code=400
            )


class GetTestKnowledgeDBAPIMixin(DBEngineAbstract):

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

    def _select_test_knowledge_from_id_sql(
            self,
            id_test_knowledge: int
    ):
        try:
            return select(TestKnowledge).where(
                cast(
                    "ColumnElement[bool]",
                    TestKnowledge.id == id_test_knowledge
                )
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select flash card from id {e}")
            raise TestKnowledgeHttpException(
                detail="Can not create select test knowledge",
                status_code=400
            )

    def _select_test_knowledge_from_id_and_user_sql(
            self,
            id_test_knowledge: int,
            user_identifier: str
    ):
        try:
            return select(TestKnowledge).where(
                and_(
                    cast(
                        "ColumnElement[bool]",
                        TestKnowledge.id == id_test_knowledge
                    ),
                    cast(
                        "ColumnElement[bool]",
                        TestKnowledge.user_identifier == user_identifier
                    ),
                )
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select flash card from id {e}")
            raise TestKnowledgeHttpException(
                detail="Can not create select test knowledge",
                status_code=400
            )

    def _select_tests_knowledge_for_user_sql(
            self,
            user_identifier: str
    ):
        try:
            return select(TestKnowledge).where(
                cast(
                    "ColumnElement[bool]",
                    TestKnowledge.user_identifier == user_identifier
                ),
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select flash card from id {e}")
            raise TestKnowledgeHttpException(
                detail="Can not create select test knowledge",
                status_code=400
            )

    def _select_test_knowledge_with_all_flash_cards_for_user_sql(
            self,
            id_knowledge: int,
            hash_identifier: str
    ):
        try:
            return select(FlashCard, TestKnowledge).where(
                and_(
                    cast(
                        "ColumnElement[bool]",
                        TestKnowledge.id == id_knowledge
                    ),
                    cast(
                        "ColumnElement[bool]",
                        TestKnowledge.hash_identifier == hash_identifier
                    ),
                )
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select flash card from test knowledge id {e}")
            raise TestKnowledgeHttpException(
                detail="Can not create select test knowledge",
                status_code=400
            )

    def query_all_tests_knowledge_generator(
            self,
            column: List[str] = None,
            order: List[str] = None
    ) -> Generator[Any]:
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

    def query_all_test_knowledge_paginate_generator(
            self,
            column: List[str] = None,
            order: List[str] = None,
            page: int = None
    ) -> Generator[Any]:
        try:
            return self.query_statement(
                self._select_all_test_knowledge_sql(column, order),
                page=page
            )
        except exc.SQLAlchemyError as e:
            logger.critical("Problem wile select all test knowledge")
            raise TestKnowledgeHttpException(
                detail="Can not select test knowledge",
                status_code=400
            )

    def query_test_knowledge_with_flash_cards_for_user(
            self,
            id_knowledge: int,
            hash_identifier: str,
    ) -> Generator[Any]:
        try:
            return self.query_statement(
                self._select_test_knowledge_with_all_flash_cards_for_user_sql(
                    id_knowledge,
                    hash_identifier
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
    ) -> Generator[Any]:
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

    def query_test_for_user(
            self,
            id_knowledge: int,
            hash_identifier: str
    ) -> Generator[Any]:
        try:
            return self.query_statement(
                self._select_test_knowledge_from_id_and_user_sql(
                    id_knowledge,
                    hash_identifier
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


    def query_tests_for_user_paginate(
            self,
            hash_identifier: str,
            page: int = None
    ) -> Generator[Any]:
        try:
            return self.query_statement(
                self._select_tests_knowledge_for_user_sql(
                    hash_identifier
                ),
                page=page
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select tests knowledge "
                f"for user {hash_identifier} -> {e}"
            )
            raise TestKnowledgeHttpException(
                detail=f"Can not select tests knowledge "
                       f"for user {hash_identifier}",
                status_code=400
            )


class UpdateKnowledgeDBAPIMixin(DBEngineAbstract):
    pass


class TestKnowledgeDBAPI(
    CreateTestKnowledgeDBAPIMixin,
    GetTestKnowledgeDBAPIMixin,
    UpdateKnowledgeDBAPIMixin,
    AnalyticsSQLMixin,
    DBEngine
):

    def get_count_test_knowledge(self):
        try:
            return next(
                self.query_statement(
                    self._count_model_sql(TestKnowledge)
                )
            ).first()
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem with count model {TestKnowledge} -> {e}"
            )
            raise TestKnowledgeHttpException(
                detail=f"Can not count model {TestKnowledge}",
                status_code=400
            )