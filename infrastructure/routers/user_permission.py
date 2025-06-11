from typing import Annotated, List, Iterator, Iterable
from fastapi import APIRouter, Depends, HTTPException, Path, Request, Body

from domain.auth.service import AuthService
from infrastructure.database.sql.api.user_permission_database import \
    UserPermissionDBAPI
from infrastructure.database.sql.models.auth import User
from infrastructure.routers.models.request.permission import \
    FullPermissionDataRequest, UserGroup, Role
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

@router.post("/", response_model=UserPermissionResponse)
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
            UserGroup(
                name=g.name,
                roles=[
                    Role(name=r.name) for r in g.roles
                ]
            ) for g in user_with_perm.user_groups]
    )


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}