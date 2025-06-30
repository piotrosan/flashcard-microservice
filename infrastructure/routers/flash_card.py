from typing import Annotated, List, Iterable, Union, Optional, Tuple

from fastapi import APIRouter, Depends, HTTPException, Path, Request, Body

from domain.flash_card.service import FashCardService
from infrastructure.database.sql.api.flash_card_database_api import FlashCardDBAPI
from infrastructure.database.sql.models import FlashCard
from infrastructure.database.sql.models.flash_card import Language
from infrastructure.routers.models.request.flash_card import \
    CreateFlashCardRequest, CreateLanguageRequest
from infrastructure.routers.models.response.flash_card import FlashCardResponse, \
    LanguageResponse
from infrastructure.security.permission.app_admin import check_admin

router = APIRouter(
    prefix="/flash-card",
    tags=["flash_card"],
    dependencies=[
        # Depends(get_token_header)
    ],
    responses={404: {"description": "Not found"}},
)

@router.get("/one/{flash_card_id}", response_model=List[FlashCardResponse])
async def get_fash_card(
        flash_card_id: Annotated[int, Path()],
        request: Request
):
    fapi = FlashCardDBAPI()
    service = FashCardService(fapi)
    fcs: Iterable[FlashCard] = service.get_flash_cards_from_ids_list(
        [flash_card_id])

    return [
        FlashCardResponse(
            id=fc.id,
            word=fc.word,
            language_id=fc.language_id,
            translate=fc.translate,
            create_at=fc.create_at,
            updated_at=fc.updated_at
        )
            for fc in fcs
    ]

@router.get("/page/{page_id}", response_model=List[FlashCardResponse])
async def get_fash_cards(
        request: Request,
        page_id: Annotated[int, Path()],
):
    fapi = FlashCardDBAPI()
    service = FashCardService(fapi)
    fcs: Iterable[Tuple[FlashCard]] = service.get_flash_cards(page_id)

    return [
        FlashCardResponse(
            id=fc[0].id,
            word=fc[0].word,
            language_id=fc[0].language_id,
            translate=fc[0].translate,
            create_at=fc[0].create_at,
            updated_at=fc[0].updated_at
        )
            for fc in fcs
    ]

@router.put(
    "/{flash_card_id}",
    response_model=dict
)
async def update_flash_card(
        request: Request,
        flash_card_id: Annotated[int, Path()],
):
    return {}


@router.post(
    "/",
    response_model=List[FlashCardResponse]
)
def create_flash_card(
        request: Request,
        flash_card_datas: Annotated[List[CreateFlashCardRequest], Body(...)]
) -> List[FlashCardResponse]:
    # check permission
    # check_admin(request.user)

    fapi = FlashCardDBAPI()
    service = FashCardService(fapi)
    fcs: Iterable[FlashCard] = service.create_flash_card(flash_card_datas)
    return [
        FlashCardResponse(
            id=fc.id,
            word=fc.word,
            language_id=fc.language_id,
            translate=fc.translate,
            create_at=fc.create_at,
            updated_at=fc.updated_at
        )
            for fc in fcs
    ]

@router.post(
    "/language",
    response_model=List[LanguageResponse]
)
def create_language(
        request: Request,
        languages: Annotated[List[CreateLanguageRequest], Body(...)]
) -> List[LanguageResponse]:
    # check permission
    # check_admin(request.user)

    fapi = FlashCardDBAPI()
    service = FashCardService(fapi)
    ls: Iterable[Language] = service.create_language(languages)
    return [
        LanguageResponse(
            id=l.id,
            shortcut=l.shortcut,
            full_name=l.full_name,
            create_at=l.create_at,
            updated_at=l.updated_at
        )
            for l in ls
    ]


@router.get(
    "/language/{page_id}",
    response_model=List[LanguageResponse]
)
def get_language(
        request: Request,
        page_id: Annotated[int, Path(...)]
) -> List[LanguageResponse]:
    # check permission
    # check_admin(request.user)

    fapi = FlashCardDBAPI()
    service = FashCardService(fapi)
    ls: Iterable[Tuple[Language]] = service.get_language()

    return [
        LanguageResponse(
            id=l[0].id,
            shortcut=l[0].shortcut,
            full_name=l[0].full_name,
            create_at=l[0].create_at,
            updated_at=l[0].updated_at
        )
            for l in ls
    ]