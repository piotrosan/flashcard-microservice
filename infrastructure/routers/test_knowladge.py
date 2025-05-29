from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Request, Body

from infrastructure.database.sql.api.test_knowledge_database_api import \
    TestKnowledgeDBAPI
from infrastructure.routers.models.request.knowledge import CreateKnowledgeRequest
from domain.test_knowledge.service import TestKnowledgeService
from infrastructure.routers.models.response.knowledge import KnowledgeResponse

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
        test_id: Annotated[int, Path()],
        request: Request
) -> KnowledgeResponse:
    dbapi = TestKnowledgeDBAPI()
    service = TestKnowledgeService(dbapi)
    result = service.get_flash_card_for_test_and_user(
        request.user.username, test_id
    )
    return KnowledgeResponse()


@router.get("/{page_id}")
async def list_test_for_user(
        page_id: Annotated[int, Path()],
        request: Request
) -> KnowledgeResponse:
    dbapi = TestKnowledgeDBAPI()
    service = TestKnowledgeService(dbapi)
    result = service.list_test_for_user()
    return KnowledgeResponse()


@router.get("/{test_id}")
async def get_test(
        test_id: Annotated[int, Path()],
        request: Request
):
    service = TestKnowledgeService()
    service.get_flash_card_for_test_and_user()



@router.post("/")
async def create_test(
        create_date: Annotated[CreateKnowledgeRequest, Body()],
        request: Request
):
    pass



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