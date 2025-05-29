from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Request, Body

from infrastructure.database.sql.api.test_knowledge_database_api import \
    TestKnowledgeDBAPI
from infrastructure.database.sql.models.test_knowledge import TestKnowledge
from infrastructure.routers.models.request.knowledge import CreateKnowledgeRequest
from domain.test_knowledge.service import TestKnowledgeService
from infrastructure.routers.models.response.knowledge import KnowledgeResponse
from infrastructure.security.permission.account_admin import check_account_admin
from infrastructure.security.permission.app_admin import check_app_admin

router = APIRouter(
    prefix="/test_knowledge",
    tags=["knowledge"],
    dependencies=[
        # Depends(get_token_header)
    ],
    responses={404: {"description": "Not found"}},
)


@router.get("/{test_id}")
async def get_test_for_user(
        id_knowledge: Annotated[int, Path()],
        request: Request
) -> KnowledgeResponse:
    dbapi = TestKnowledgeDBAPI()
    service = TestKnowledgeService(dbapi)
    result = service.get_test_for_user(
        id_knowledge,
        request.user.username
    )
    return KnowledgeResponse()


@router.get("/{page_id}")
async def list_test_for_user(
        page_id: Annotated[int, Path()],
        request: Request
) -> KnowledgeResponse:
    dbapi = TestKnowledgeDBAPI()
    service = TestKnowledgeService(dbapi)
    result = service.list_test_for_user(
        request.user.username,
        page_id=page_id
    )
    return KnowledgeResponse()


@router.get("/{test_id}")
async def get_test(
        id_knowledge: Annotated[int, Path()],
        request: Request
) -> KnowledgeResponse:
    assert check_app_admin(request.user)
    dbapi = TestKnowledgeDBAPI()
    service = TestKnowledgeService(dbapi)
    service.get_test(id_knowledge)
    return KnowledgeResponse()


@router.post("/")
async def create_test(
        create_date: Annotated[CreateKnowledgeRequest, Body()],
        request: Request
) -> KnowledgeResponse:
    assert check_account_admin(request.user)
    dbapi = TestKnowledgeDBAPI()
    service = TestKnowledgeService(dbapi)
    saved_object: TestKnowledge = service.insert(create_date).pop()
    return KnowledgeResponse(**saved_object.__dict__)

# @router.put(
#     "/{item_id}",
#     tags=["custom"],
#     responses={403: {"description": "Operation forbidden"}},
# )
# async def update_item(item_id: str):
#     if item_id != "plumbus":
#         raise HTTPException(
#             status_code=403, detail="You can only update the item: plumbus"
#         )
#     return {"item_id": item_id, "name": "The great Plumbus"}