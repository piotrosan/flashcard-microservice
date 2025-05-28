from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Request

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