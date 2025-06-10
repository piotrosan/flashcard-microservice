import logging
from typing import Iterable, List, cast, Generator, Iterator

from typing_extensions import Any

from sqlalchemy import select, text, and_
from sqlalchemy import exc

from infrastructure.database.sql.api.engine import DBEngine, DBEngineAbstract
from infrastructure.database.sql.models import UserGroup
from infrastructure.database.sql.models.auth import User, Role, \
    association_user_user_group
from infrastructure.database.sql.api.exception.test_knowledge_exception import TestKnowledgeHttpException

logger = logging.getLogger("root")


class CreateUserPermissionsDBAPIMixin(DBEngineAbstract):

    def insert(
            self,
            full_permission_data: dict
    ) -> User:
        try:
            user = User(
                hash_identifier=full_permission_data['hash_identifier']
            )
            list_groups = []
            for g in full_permission_data['user_groups']:
                ug = UserGroup(name=g['name'])
                for r in g['roles']:
                    ro = Role(
                        name=r['name'],
                        user_group_id=ug
                    )

                list_groups.append(ug)

            self.insert_objects([user])
            self.insert_objects(list_groups)
            associations = [
                association_user_user_group(user=user, groups=g)
                for g in list_groups
            ]
            self.insert_objects(associations)
            return user
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile insert user permission -> {e}"
            )
            raise TestKnowledgeHttpException(
                detail="Can not insert user permission",
                status_code=400
            )


class GetTestKnowledgeDBAPIMixin(DBEngineAbstract):
    pass
    # def _select_all_test_knowledge_sql(
    #         self,
    #         column: List[str] = None,
    #         order: List[str] = None
    # ):
    #     tmp_select = select(TestKnowledge)
    #
    #     if column:
    #         tmp_select.column(*[text(col) for col in column])
    #
    #     if order:
    #         tmp_select.order_by(*[text(col) for col in order])
    #
    #     return tmp_select
    #
    # def _select_test_knowledge_from_id_sql(
    #         self,
    #         id_test_knowledge: int
    # ):
    #     try:
    #         return select(TestKnowledge).where(
    #             cast(
    #                 "ColumnElement[bool]",
    #                 TestKnowledge.id == id_test_knowledge
    #             )
    #         )
    #     except exc.SQLAlchemyError as e:
    #         logger.critical(
    #             f"Problem wile select flash card from id {e}")
    #         raise TestKnowledgeHttpException(
    #             detail="Can not create select test knowledge",
    #             status_code=400
    #         )
    #
    # def _select_test_knowledge_from_id_and_user_sql(
    #         self,
    #         id_test_knowledge: int,
    #         user_identifier: str
    # ):
    #     try:
    #         return select(TestKnowledge).where(
    #             and_(
    #                 cast(
    #                     "ColumnElement[bool]",
    #                     TestKnowledge.id == id_test_knowledge
    #                 ),
    #                 cast(
    #                     "ColumnElement[bool]",
    #                     TestKnowledge.user_identifier == user_identifier
    #                 ),
    #             )
    #         )
    #     except exc.SQLAlchemyError as e:
    #         logger.critical(
    #             f"Problem wile select flash card from id {e}")
    #         raise TestKnowledgeHttpException(
    #             detail="Can not create select test knowledge",
    #             status_code=400
    #         )
    #
    # def _select_tests_knowledge_for_user_sql(
    #         self,
    #         user_identifier: str
    # ):
    #     try:
    #         return select(TestKnowledge).where(
    #             cast(
    #                 "ColumnElement[bool]",
    #                 TestKnowledge.user_identifier == user_identifier
    #             ),
    #         )
    #     except exc.SQLAlchemyError as e:
    #         logger.critical(
    #             f"Problem wile select flash card from id {e}")
    #         raise TestKnowledgeHttpException(
    #             detail="Can not create select test knowledge",
    #             status_code=400
    #         )
    #
    # def _select_test_knowledge_with_all_flash_cards_for_user_sql(
    #         self,
    #         id_knowledge: int,
    #         hash_identifier: str
    # ):
    #     try:
    #         return select(FlashCard, TestKnowledge).where(
    #             and_(
    #                 cast(
    #                     "ColumnElement[bool]",
    #                     TestKnowledge.id == id_knowledge
    #                 ),
    #                 cast(
    #                     "ColumnElement[bool]",
    #                     TestKnowledge.hash_identifier == hash_identifier
    #                 ),
    #             )
    #         )
    #     except exc.SQLAlchemyError as e:
    #         logger.critical(
    #             f"Problem wile select flash card from test knowledge id {e}")
    #         raise TestKnowledgeHttpException(
    #             detail="Can not create select test knowledge",
    #             status_code=400
    #         )
    #
    # def query_all_tests_knowledge_generator(
    #         self,
    #         column: List[str] = None,
    #         order: List[str] = None
    # ) -> Iterator[Any]:
    #     try:
    #         return self.query_statement(
    #             self._select_all_test_knowledge_sql(column, order)
    #         )
    #     except exc.SQLAlchemyError as e:
    #         logger.critical("Problem wile select all test knowledge")
    #         raise TestKnowledgeHttpException(
    #             detail="Can not select test knowledge",
    #             status_code=400
    #         )
    #
    # def query_all_test_knowledge_paginate_generator(
    #         self,
    #         column: List[str] = None,
    #         order: List[str] = None,
    #         page: int = None
    # ) -> Iterator[Any]:
    #     try:
    #         return self.query_statement(
    #             self._select_all_test_knowledge_sql(column, order),
    #             page=page
    #         )
    #     except exc.SQLAlchemyError as e:
    #         logger.critical("Problem wile select all test knowledge")
    #         raise TestKnowledgeHttpException(
    #             detail="Can not select test knowledge",
    #             status_code=400
    #         )
    #
    # def query_test_knowledge_with_flash_cards_for_user(
    #         self,
    #         id_knowledge: int,
    #         hash_identifier: str,
    # ) -> Iterator[Any]:
    #     try:
    #         return self.query_statement(
    #             self._select_test_knowledge_with_all_flash_cards_for_user_sql(
    #                 id_knowledge,
    #                 hash_identifier
    #             )
    #         )
    #     except exc.SQLAlchemyError as e:
    #         logger.critical(
    #             f"Problem wile select test knowledge {id_knowledge} -> {e}"
    #         )
    #         raise TestKnowledgeHttpException(
    #             detail=f"Can not select test knowledge {id_knowledge}",
    #             status_code=400
    #         )
    #
    # def query_test_knowledge_from_id(
    #         self,
    #         id_knowledge: int
    # ) -> Iterator[Any]:
    #     try:
    #         return self.query_statement(
    #             self._select_test_knowledge_from_id_sql(id_knowledge)
    #         )
    #     except exc.SQLAlchemyError as e:
    #         logger.critical(
    #             f"Problem wile select test knowledge {id_knowledge} -> {e}"
    #         )
    #         raise TestKnowledgeHttpException(
    #             detail=f"Can not select test knowledge {id_knowledge}",
    #             status_code=400
    #         )
    #
    # def query_test_for_user(
    #         self,
    #         id_knowledge: int,
    #         hash_identifier: str
    # ) -> Iterator[Any]:
    #     try:
    #         return self.query_statement(
    #             self._select_test_knowledge_from_id_and_user_sql(
    #                 id_knowledge,
    #                 hash_identifier
    #             )
    #         )
    #     except exc.SQLAlchemyError as e:
    #         logger.critical(
    #             f"Problem wile select test knowledge {id_knowledge} -> {e}"
    #         )
    #         raise TestKnowledgeHttpException(
    #             detail=f"Can not select test knowledge {id_knowledge}",
    #             status_code=400
    #         )
    #
    #
    # def query_tests_for_user_paginate(
    #         self,
    #         hash_identifier: str,
    #         page: int = None
    # ) -> Iterator[Any]:
    #     try:
    #         return self.query_statement(
    #             self._select_tests_knowledge_for_user_sql(
    #                 hash_identifier
    #             ),
    #             page=page
    #         )
    #     except exc.SQLAlchemyError as e:
    #         logger.critical(
    #             f"Problem wile select tests knowledge "
    #             f"for user {hash_identifier} -> {e}"
    #         )
    #         raise TestKnowledgeHttpException(
    #             detail=f"Can not select tests knowledge "
    #                    f"for user {hash_identifier}",
    #             status_code=400
    #         )


class UpdateKnowledgeDBAPIMixin(DBEngineAbstract):
    pass


class UserPermissionDBAPI(
    CreateUserPermissionsDBAPIMixin,
    # GetTestKnowledgeDBAPIMixin,
    # UpdateKnowledgeDBAPIMixin,
    DBEngine
):
    pass