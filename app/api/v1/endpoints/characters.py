"""
Characters routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.character import CharacterSchema, CharacterCreateSchema, CharacterUpdateSchema
from app.api.v1.dependencies import get_db, get_current_user
from app.crud import character as crud
from app.models.user import User
from app.api.v1.endpoints import character_errors as error_details


router = APIRouter()


@router.get('/', response_model=list[CharacterSchema])
def read_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Read characters"""
    return crud.get_characters(db, user_owner_id=current_user.user_id)


@router.get('/{character_id}', response_model=CharacterSchema)
def read_one(character_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get character by id"""
    character = crud.get_user_character_by_id(character_id=character_id, user_id=current_user.user_id, db=db)
    if character is None:
        raise HTTPException(status_code=404)
    else:
        return character


@router.put('/{character_id}', response_model=CharacterSchema)
def update(character_id: int,
           character: CharacterUpdateSchema,
           current_user: User = Depends(get_current_user),
           db: Session = Depends(get_db)):
    """Update character"""
    # check if the user owns the character
    if not current_user.owns_character(character_id):
        raise HTTPException(status_code=404, detail=error_details.CHARACTER_NOT_FOUND)
    # update the character
    return crud.update_character(db, character_id, character)


@router.post('/', response_model=CharacterSchema, status_code=201)
def create(character: CharacterCreateSchema,
           db: Session = Depends(get_db),
           current_user: User = Depends(get_current_user)):
    """Create new character"""
    return crud.create_character(db, character, current_user.user_id)


@router.delete('/{character_id}')
def delete(character_id: int,
           db: Session = Depends(get_db),
           current_user: User = Depends(get_current_user)):
    """Delete character"""
    # check if the user owns the character
    if not current_user.owns_character(character_id):
        raise HTTPException(status_code=404, detail=error_details.CHARACTER_NOT_FOUND)
    crud.disable_character(db, character_id)
