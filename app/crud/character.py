"""
CRUD operations for Characters
"""

from typing import Union
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.character import Character
from app.schemas.character import CharacterCreateSchema, CharacterUpdateSchema


def get_characters(db: Session,
                   q: str = None,
                   user_owner_id: int = None,
                   offset: int = 0,
                   limit: int = 100) -> Union[list[Character], list]:
    """
    Get list of characters from database
    :param db:
    :param q: search filter query
    :param user_owner_id: filter by owner id
    :param offset:
    :param limit:
    :return:
    """
    characters = db.query(Character)
    if user_owner_id:
        characters = characters.filter(Character.user_owner_id == user_owner_id)
    if q:
        characters = characters.filter(
            Character.name.like(f'%{q}%')
        )
    return characters.order_by(Character.character_id.asc()).offset(offset).limit(limit).all()


def get_character_by_id(db: Session, character_id: int) -> Union[Character, None]:
    """
    Get character by id
    :param db:
    :param character_id:
    :return:
    """
    character = db.get(Character, character_id)
    if character:
        return character
    else:
        return None


def get_user_character_by_id(db: Session, user_id: int, character_id: int) -> Union[Character, None]:
    """
    Get character by id filtered by user owner id
    :param db:
    :param user_id: character owner id
    :param character_id:
    :return:
    """
    character = db.query(Character).filter(and_(
        Character.user_owner_id == user_id,
        Character.character_id == character_id
    )).first()
    if character:
        return character
    else:
        return None


def create_character(db: Session, character: CharacterCreateSchema, user_owner_id: int) -> Character:
    """
    Create new character
    :param db:
    :param character:
    :param user_owner_id:
    :return:
    """
    new_character = Character(user_owner_id=user_owner_id, **character.dict(exclude_unset=True), )
    db.add(new_character)
    db.commit()
    db.refresh(new_character)
    return new_character


def update_character(db: Session, character_id: int, character: CharacterUpdateSchema) -> Union[Character, None]:
    """
    Update character
    :param db:
    :param character_id:
    :param character:
    :return:
    """
    existing_character = db.get(Character, character_id)
    if existing_character is None:
        return None
    else:
        for var, value in character.dict(exclude_unset=False).items():
            setattr(existing_character, var, value)
        db.commit()
        return existing_character


def disable_character(db: Session, character_id: int) -> Union[None, bool]:
    """
    Disable character by id
    :param db:
    :param character_id:
    :return:
    """
    character = db.get(Character, character_id)
    if character is None:
        return None
    else:
        try:
            character.disabled = True
            db.commit()
            return True
        except:
            # todo: need to log exception in disable_character
            return False
