"""
Item routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.item import ItemSchema, ItemCreateSchema, ItemUpdateSchema
from app.api.dependencies import get_db
from app.crud import item as crud


router = APIRouter()


@router.get('/', response_model=list[ItemSchema])
def read_all(db: Session = Depends(get_db)):
    """Read items"""
    return crud.get_items(db)


@router.get('/{item_id}', response_model=ItemSchema)
def read_one(item_id: int, db: Session = Depends(get_db)):
    """Get item by id"""
    item = crud.get_item_by_id(item_id=item_id, db=db)
    if item is None:
        raise HTTPException(status_code=404)
    else:
        return item


@router.put('/{item_id}', response_model=ItemSchema)
def update(item_id: int, item: ItemUpdateSchema, db: Session = Depends(get_db)):
    """Update item"""
    item = crud.update_item(db, item_id, item)
    if item is None:
        raise HTTPException(status_code=404)
    else:
        return item


@router.post('/', response_model=ItemSchema)
def create(item: ItemCreateSchema, db: Session = Depends(get_db)):
    """Create new item"""
    return crud.create_item(db, item)


@router.delete('/{item_id}')
def delete(item_id: int, db: Session = Depends(get_db)):
    """Delete item"""
    response = crud.disable_item(db, item_id)
    if response is None:
        raise HTTPException(status_code=404)
