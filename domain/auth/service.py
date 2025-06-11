from typing import List, Iterable

from infrastructure.database.sql.api.flash_card_database_api import FlashCardDBAPI
from infrastructure.database.sql.api.user_permission_database import \
    UserPermissionDBAPI
from infrastructure.database.sql.models.auth import User
from infrastructure.routers.models.request.permission import \
    FullPermissionDataRequest


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


    def get_flash_card(self, flash_card: int):
        pass
