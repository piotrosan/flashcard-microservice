from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Request

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/test_knowledge",
    tags=["knowledge"],
    dependencies=[
        # Depends(get_token_header)
    ],
    responses={404: {"description": "Not found"}},
)

@router.get("/{test_id}")
async def get_test(test_id: Annotated[int, Path()], request: Request):





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