"""
CRUD operations for Adventure
"""

from typing import Union
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, tuple_

from app.models.adventure import Adventure
from app.schemas.adventure import AdventureCreateSchema, AdventureUpdateSchema


def get_adventures(db: Session,
                   q: str = None,
                   offset: int = 0,
                   limit: int = 100) -> Union[list[Adventure], list]:
    """
    Get list of adventures from database
    :param db:
    :param q: search filter query
    :param offset:
    :param limit:
    :return:
    """
    adventures = db.query(Adventure) \
        .filter(
            tuple_(Adventure.adventure_id, Adventure.aid)
            .in_(
                db.query(Adventure.adventure_id, func.max(Adventure.aid).label('last_id'))
                .group_by(Adventure.adventure_id)
            )
        )

    if q:
        adventures = adventures.filter(or_(
            Adventure.name.like(f'%{q}%'),
            Adventure.plot.like(f'%{q}%')
        ))
    return adventures.order_by(Adventure.adventure_id.asc()).offset(offset).limit(limit).all()


def get_adventure_by_aid(db: Session, aid: int) -> Union[Adventure, None]:
    """
    Get adventure by its id (NOT original id)
    :param db:
    :param aid:
    :return:
    """
    return db.get(Adventure, aid)


def get_adventure_by_id(db: Session, adventure_id: int) -> Union[Adventure, None]:
    """
    Get the most recent adventure version by its id (but not by aid)
    :param db:
    :param adventure_id:
    :return:
    """
    return db.query(Adventure) \
        .filter(Adventure.adventure_id == adventure_id) \
        .order_by(Adventure.aid.desc()) \
        .first()


def create_adventure(db: Session, adventure: AdventureCreateSchema) -> Adventure:
    """
    Create new adventure
    :param db:
    :param adventure:
    :return: new adventure data
    """
    adventure = Adventure(**adventure.dict())
    db.add(adventure)
    db.flush()
    adventure.adventure_id = adventure.aid
    db.commit()
    db.refresh(adventure)
    return adventure


def disable_adventure(db: Session, adventure_id: int) -> Union[int, None]:
    """
    Change adventure status to disabled
    :param db:
    :param adventure_id:
    :return: disabled adventure original id or None if adventure not found
    """
    adventure = get_adventure_by_id(db, adventure_id)
    if adventure is None:
        return None
    else:
        adventure.is_active = False
        db.commit()
        return adventure.adventure_id


def update_adventure(
        db: Session,
        adventure_id: int,
        adventure: AdventureUpdateSchema
) -> Union[Adventure, None]:
    """
    Update Adventure
    :param db:
    :param adventure_id:
    :param adventure:
    :return:
    """
    existing_adventure = get_adventure_by_id(db, adventure_id)
    if existing_adventure is None:
        return None
    # if existing adventure is locked by some gametable, then create a new one with the same original id
    if existing_adventure.is_locked:
        new_adventure = Adventure(**adventure.dict(exclude_unset=True))
        new_adventure.adventure_id = existing_adventure.adventure_id
        db.add(new_adventure)
        db.commit()
        return new_adventure
    # if adventure is not locked, then just update current one
    else:
        for var, value in adventure.dict(exclude_unset=True).items():
            setattr(existing_adventure, var, value)
        db.commit()
        return existing_adventure
