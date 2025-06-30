from typing import Annotated, Iterator, Tuple, List
from fastapi import APIRouter, HTTPException, Path, Request, Body, WebSocket

from infrastructure.database.sql.api.test_knowledge_database_api import \
    TestKnowledgeDBAPI
from infrastructure.database.sql.models import FlashCard
from infrastructure.database.sql.models.test_knowledge import TestKnowledge
from infrastructure.routers.models.request.generic import GenericRequest
from infrastructure.routers.models.request.knowledge import \
    CreateKnowledgeRequest, UpdateKnowledgeRequest
from domain.test_knowledge.service import TestKnowledgeService
from infrastructure.routers.models.response.flash_card import FlashCardResponse
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

@router.get(
    "/tst/fsh_crd/lang/{id_test_knowledge}",
    response_model=List[KnowledgeResponse]
)
async def get_test_with_all_data_for_user(
        id_test_knowledge: Annotated[int, Path()],
        request: Request
) -> List[KnowledgeResponse]:
    dbapi = TestKnowledgeDBAPI()
    service = TestKnowledgeService(dbapi)
    tsts_know: Iterator[
        Tuple[TestKnowledge]
    ] = service.get_tsts_know_with_cards_for_user(
        request.user.hash_identifier,
        id_test_knowledge=id_test_knowledge
    )
    fc: FlashCard
    return [
        KnowledgeResponse(
            id=tst[0].id,
            planned_start=tst[0].planned_start,
            create_at=tst[0].create_at,
            updated_at=tst[0].updated_at,
            flash_cards=[FlashCardResponse(
                id=fc.id,
                word=fc.word,
                translate=fc.translate,
                language_id=fc.language.full_name,
                create_at=fc.create_at,
                updated_at=fc.updated_at
            )
                for fc in tst[0].flash_cards
            ]
        )
        for tst in tsts_know
    ]




@router.post("/", response_model=KnowledgeResponse)
async def create_test(
        create_date: Annotated[CreateKnowledgeRequest, Body()],
        request: Request
) -> KnowledgeResponse:
    # assert check_account_admin(request.user.hash_identifier)
    dbapi = TestKnowledgeDBAPI()
    service = TestKnowledgeService(dbapi)
    saved_object: TestKnowledge = service.insert(create_date)
    return KnowledgeResponse(**saved_object.__dict__)


@router.websocket("/play_random")
async def play_random(websocket: WebSocket, request: Request):
    dbapi = TestKnowledgeDBAPI()
    service = TestKnowledgeService(dbapi)
    statistics = {}
    test_knowledge_with_content: Iterator[TestKnowledge] = \
        service.get_random_tsts_know_with_cards_for_user(request.user)
    test = next(test_knowledge_with_content)
    flsh_crds: List[FlashCard] = test.flash_cards

    await websocket.accept()
    while flsh_crds:
        await websocket.send_json(flsh_crds.pop(0).__dict__)
        result = await websocket.receive_json()
        if result['correct']:
            statistics[result['word']] = True
        else:
            statistics[result['word']] = False

    await websocket.send_text('Test have been finish')
    return GenericRequest(message='object have been updated')