from typing import Annotated, List, Iterable

from fastapi import APIRouter, Depends, HTTPException, Path, Request, Body

from domain.flash_card.service import FashCardService
from infrastructure.database.sql.api.flash_card_database_api import FlashCardDBAPI
from infrastructure.database.sql.models import FlashCard
from infrastructure.routers.models.request.flash_card import CreateFlashCardRequest
from infrastructure.routers.models.response.flash_card import FlashCardResponse
from infrastructure.security.permission.app_admin import check_admin

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/flash-card",
    tags=["flash_card"],
    dependencies=[
        # Depends(get_token_header)
    ],
    responses={404: {"description": "Not found"}},
)

@router.get("/{flash_card_id}")
async def get_fash_card(
        flash_card_id: Annotated[int, Path()],
        request: Request
):
    pass

@router.get("/")
async def list_fash_cards(request: Request):
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


@router.post(
    "/",
    response_model=List[FlashCardResponse]
)
async def create_flash_card(
        request: Request,
        flash_card_datas: Annotated[List[CreateFlashCardRequest], Body(...)]
) -> List[FlashCardResponse]:
    # check permission
    check_admin(request.user)

    fapi = FlashCardDBAPI()
    service = FashCardService(fapi)
    fcs: Iterable[FlashCard] = service.create_flash_card(flash_card_datas)
    return [
        FlashCardResponse(
            id=fc.id,
            word=fc.word,
            translate=fc.translate,
            create_at=fc.create_at,
            updated_at=fc.updated_at
        )
            for fc in fcs
    ]