"""
Characters routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.character import CharacterSchema, CharacterCreateSchema, CharacterUpdateSchema
from app.api.dependencies import get_db
from app.crud import character as crud


router = APIRouter(
    prefix='/characters',
    tags=['characters']
)


@router.get('/', response_model=list[CharacterSchema])
def read_all(db: Session = Depends(get_db)):
    """Read characters"""
    return crud.get_characters(db)


@router.get('/{character_id}', response_model=CharacterSchema)
def read_one(character_id: int, db: Session = Depends(get_db)):
    """Get character by id"""
    character = crud.get_character_by_id(character_id=character_id, db=db)
    if character is None:
        raise HTTPException(status_code=404)
    else:
        return character


@router.put('/{character_id}', response_model=CharacterSchema)
def update(character_id: int, character: CharacterUpdateSchema, db: Session = Depends(get_db)):
    """Update character"""
    character = crud.update_character(db, character_id, character)
    if character is None:
        raise HTTPException(status_code=404)
    else:
        return character


@router.post('/', response_model=CharacterSchema)
def create(character: CharacterCreateSchema, db: Session = Depends(get_db)):
    """Create new character"""
    user_owner_id = 1
    return crud.create_character(db, character, user_owner_id)


@router.delete('/{character_id}')
def delete(character_id: int, db: Session = Depends(get_db)):
    """Delete character"""
    response = crud.disable_character(db, character_id)
    if response is None:
        raise HTTPException(status_code=404)
