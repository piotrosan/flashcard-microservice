from typing import Annotated, List, Iterator, Iterable
from fastapi import APIRouter, Depends, HTTPException, Path, Request, Body

from domain.auth.service import AuthService
from infrastructure.database.sql.api.user_permission_database import \
    UserPermissionDBAPI
from infrastructure.database.sql.models.auth import User, UserGroup
from infrastructure.routers.models.request.permission import \
    FullPermissionDataRequest, UserGroupAndRole, Role, UserAndGroup
from infrastructure.routers.models.response.permission import \
    UserPermissionResponse

router = APIRouter(
    prefix="/permission",
    tags=["user permission"],
    dependencies=[
        # Depends(get_token_header)
    ],
    responses={404: {"description": "Not found"}},
)

@router.post("/user_group_role", response_model=UserPermissionResponse)
async def set_user_group_and_permission(
    full_permission_data: Annotated[
        FullPermissionDataRequest, Body(...)
    ],
    request: Request
):
    up_db = UserPermissionDBAPI()
    ats = AuthService(up_db)
    user: User = ats.save_user_permission(full_permission_data)
    user_with_perm = ats.get_user_with_permission(
        user.hash_identifier)
    return UserPermissionResponse(
        hash_identifier=user_with_perm.hash_identifier,
        user_groups=[
            UserGroupAndRole(
                name=g.name,
                roles=[
                    Role(name=r.name) for r in g.roles
                ]
            ) for g in user_with_perm.user_groups]
    )


@router.post(
    "/group_role",
    response_model=List[UserGroupAndRole]
)
async def save_group_and_role(
    permission_data: Annotated[
        List[UserGroupAndRole], Body(...)
    ],
    request: Request
):
    up_db = UserPermissionDBAPI()
    ats = AuthService(up_db)
    groups: List[UserGroup] = ats.save_groups_and_roles(permission_data)

    return [
        UserGroupAndRole(
            name=g.name,
            roles=[Role(name=r.name) for r in g.roles]
        ) for g in groups]


@router.put(
    "/add_user_to_role",
    response_model=int
)
async def add_user_to_group(
    permission_data: Annotated[
        UserAndGroup, Body(...)
    ],
    request: Request
):
    up_db = UserPermissionDBAPI()
    ats = AuthService(up_db)
    amount: int = ats.add_user_to_group(permission_data)
    return amount

