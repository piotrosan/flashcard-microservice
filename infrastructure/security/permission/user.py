from typing import List

from infrastructure.database.sql.models import UserGroup
from infrastructure.database.sql.models.auth import User


def check_app_user(user: User) -> bool:
    ugs: List[UserGroup] = user.user_groups

    result = [
        ug.name == 'user'
        for ug in ugs
    ]
    return all(result)
