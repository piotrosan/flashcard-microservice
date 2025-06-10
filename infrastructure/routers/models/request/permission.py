from typing import List
from pydantic import BaseModel

class Role(BaseModel):
    name: str

class UserGroup(BaseModel):
    name: str
    roles: List[Role]

class FullPermissionDataRequest(BaseModel):
    user_groups: List[UserGroup]
    hash_identifier: str
