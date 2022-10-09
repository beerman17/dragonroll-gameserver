"""
Adventures routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.adventure import AdventureUpdateSchema, AdventureCreateSchema, AdventureSchema
from app.api.dependencies import get_db
from app.crud import adventure as crud


router = APIRouter()


@router.get('/', response_model=list[AdventureSchema])
def read_all(db: Session = Depends(get_db)):
    """
    Get list of adventures from database
    """
    return crud.get_adventures(db)


@router.get('/{adventure_id}', response_model=AdventureSchema)
def read_one(adventure_id: int, db: Session = Depends(get_db)):
    """
    Get adventure by id
    """
    adventure = crud.get_adventure_by_id(db, adventure_id)
    if adventure is None:
        raise HTTPException(status_code=404)
    else:
        return adventure


@router.put('/{adventure_id}', response_model=AdventureSchema)
def update(adventure_id: int, adventure: AdventureUpdateSchema, db: Session = Depends(get_db)):
    """
    Update adventure
    """
    adventure = crud.update_adventure(db, adventure_id, adventure)
    if adventure is None:
        raise HTTPException(status_code=404)
    else:
        return adventure


@router.post('/', response_model=AdventureSchema)
def create(adventure: AdventureCreateSchema, db: Session = Depends(get_db)):
    """
    Create new adventure
    """
    return crud.create_adventure(db, adventure)


@router.delete('/{adventure_id}')
def delete(adventure_id: int, db: Session = Depends(get_db)):
    """
    Delete adventure
    """
    crud.disable_adventure(db, adventure_id)
