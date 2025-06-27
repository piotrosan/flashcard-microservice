from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Request, Body, WebSocket

from infrastructure.database.sql.api.test_knowledge_database_api import \
    TestKnowledgeDBAPI
from infrastructure.database.sql.models.test_knowledge import TestKnowledge
from infrastructure.routers.models.request.generic import GenericRequest
from infrastructure.routers.models.request.knowledge import \
    CreateKnowledgeRequest, UpdateKnowledgeRequest
from domain.test_knowledge.service import TestKnowledgeService
from infrastructure.routers.models.response.knowledge import KnowledgeResponse
from infrastructure.security.permission.account_admin import check_account_admin
from infrastructure.security.permission.app_admin import check_admin

router = APIRouter(
    prefix="/test_knowledge",
    tags=["knowledge"],
    dependencies=[
        # Depends(get_token_header)
    ],
    responses={404: {"description": "Not found"}},
)


@router.get("/{test_id}", response_model=KnowledgeResponse)
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


@router.get("/{page_id}", response_model=KnowledgeResponse)
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


@router.get("/{test_id}", response_model=KnowledgeResponse)
async def get_test(
        id_knowledge: Annotated[int, Path()],
        request: Request
) -> KnowledgeResponse:
    dbapi = TestKnowledgeDBAPI()
    service = TestKnowledgeService(dbapi)
    service.get_test(id_knowledge)
    return KnowledgeResponse()


@router.post("/", response_model=KnowledgeResponse)
async def create_test(
        create_date: Annotated[CreateKnowledgeRequest, Body()],
        request: Request
) -> KnowledgeResponse:
    assert check_account_admin(request.user.hash_identifier)
    dbapi = TestKnowledgeDBAPI()
    service = TestKnowledgeService(dbapi)
    saved_object: TestKnowledge = service.insert(create_date).pop()
    return KnowledgeResponse(**saved_object.__dict__)

@router.put(
    "/",
    response_model=GenericRequest
)
async def update_test(
        test_data: Annotated[
            UpdateKnowledgeRequest, Body()
        ]
):
    dbapi = TestKnowledgeDBAPI()
    service = TestKnowledgeService(dbapi)
    service.update_test(test_data)
    return GenericRequest(message='object have been updated')


@router.websocket("/play")
async def play_random(websocket: WebSocket, request: Request):
    dbapi = TestKnowledgeDBAPI()
    service = TestKnowledgeService(dbapi)
    statistics = {}
    test_knowledge_with_content = service.get_random_test_for_user(request.user)
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(
            f"Session cookie or query token value is: {cookie_or_token}"
        )
        if q is not None:
            await websocket.send_text(f"Query parameter q is: {q}")
        await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")
    return GenericRequest(message='object have been updated')