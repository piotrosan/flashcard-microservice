import logging
from typing import Iterable, List, cast, Generator, Iterator

from sqlalchemy.orm import contains_eager, joinedload
from typing_extensions import Any

from sqlalchemy import select, text, and_
from sqlalchemy import exc

from infrastructure.database.sql.api.engine import DBEngine, DBEngineAbstract
from infrastructure.database.sql.api.exception.auth_exception import \
    AuthHttpException
from infrastructure.database.sql.models import UserGroup
from infrastructure.database.sql.models.auth import User, Role, AssociationUserGroupUser
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

            groups = []
            for g in full_permission_data['user_groups']:
                ug = UserGroup(name=g['name'])
                list_roles = []
                for r in g['roles']:
                    ro = Role(
                        name=r['name'],
                        user_group_id=ug
                    )
                    list_roles.append(ro)
                ug.roles = list_roles
                groups.append(ug)

            associations = [
                AssociationUserGroupUser(user=user, user_group=g)
                for g in groups
            ]

            self.insert_objects([user] + associations)
            return user
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile insert user permission -> {e}"
            )
            raise TestKnowledgeHttpException(
                detail="Can not insert user permission",
                status_code=400
            )


class GetUserPermissionDBAPIMixin(DBEngineAbstract):
    def _select_all_test_knowledge_sql(
            self,
            column: List[str] = None,
            order: List[str] = None
    ):
        tmp_select = select(User)

        if column:
            tmp_select.column(*[text(col) for col in column])

        if order:
            tmp_select.order_by(*[text(col) for col in order])

        return tmp_select

    def _select_user_with_permisison_sql(
            self,
            hash_identifier: str
    ):
        return (
            select(User)
            .join_from(
                User,
                UserGroup,
                User.user_groups.any(
                    and_(
                        AssociationUserGroupUser.left_user_id == User.id,
                        AssociationUserGroupUser.right_user_group_id == UserGroup.id,
                        User.hash_identifier == hash_identifier
                    )
                )
            )
            .join_from(
                UserGroup,
                Role,
                and_(
                    UserGroup.id == Role.user_group_id
                )
            )
            .where(
                cast(
                    "ColumnElement[bool]",
                    User.hash_identifier == hash_identifier
                )
            )
            .options(joinedload(User.user_groups).joinedload(UserGroup.roles))
        )

    def query_user_with_permission_paginate_generator(
            self,
            hash_identifier: str,
            page: int = None
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                self._select_user_with_permisison_sql(hash_identifier),
                page=page
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                "Problem wile select query"
                f" user with permission - {e}")
            raise AuthHttpException(
                detail="Can not select user",
                status_code=400
            )

class UpdateUserPermissionDBAPIMixin(DBEngineAbstract):
    pass


class UserPermissionDBAPI(
    CreateUserPermissionsDBAPIMixin,
    GetUserPermissionDBAPIMixin,
    UpdateUserPermissionDBAPIMixin,
    DBEngine
):
    pass