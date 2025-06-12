from typing import List, Iterable

from infrastructure.database.sql.api.flash_card_database_api import FlashCardDBAPI
from infrastructure.database.sql.api.user_permission_database import \
    UserPermissionDBAPI
from infrastructure.database.sql.models.auth import User, UserGroup, Role
from infrastructure.routers.models.request.permission import \
    FullPermissionDataRequest, UserGroupAndRole, UserAndGroup


class AuthService:

    def __init__(self, infrastructure_db: UserPermissionDBAPI):
        self.infrastructure_db = infrastructure_db

    def save_user_permission(
            self, full_permission_data: FullPermissionDataRequest
    ) -> User:
        return self.infrastructure_db.insert(
            full_permission_data.model_dump(mode='Python')
        )

    def get_user_with_permission(self, hash_identifier: str) -> User:
        res =  next(
            self.infrastructure_db.query_user_with_permission_paginate_generator(
                hash_identifier
            )
        )
        return res[0]

    def save_groups_and_roles(
            self,
            groups_and_role: List[UserGroupAndRole]
    ) -> List[UserGroup]:
        return self.infrastructure_db.insert_group_and_role(
            groups_and_role
        )


    def add_user_to_group(
            self,
            user_and_groups: UserAndGroup
    ) -> int:
        ug: List[UserGroup] = self.infrastructure_db.query_groups_for_names(
            user_and_groups.name
        )
        user: User = self.infrastructure_db.query_user_from_hash(
            user_and_groups.hash_identifier)
        amount_of_added = self.infrastructure_db.add_user_to_group(ug, user)
        return amount_of_added


    def update_group_from_id(
            self,
            group_id: int,
            new_name: str
    ) -> UserGroup:
        return self.infrastructure_db.update_group_from_id(
            group_id, new_name)

    def update_role_from_id(
            self,
            role_id: int,
            new_name: str
    ) -> Role:
        return self.infrastructure_db.update_role_from_id(
            role_id, new_name)
