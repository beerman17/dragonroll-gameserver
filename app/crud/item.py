"""
CRUD operations for Items
"""

from typing import Union
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.item import Item
from app.schemas.item import ItemCreateSchema, ItemUpdateSchema


def get_items(db: Session,
              q: str = None,
              offset: int = 0,
              limit: int = 100) -> Union[list[Item], list]:
    """
    Get list of items from database
    :param db:
    :param q: search filter query
    :param offset:
    :param limit:
    :return:
    """
    items = db.query(Item)
    if q:
        items = items.filter(
            or_(
                Item.name.like(f'%{q}%'),
                Item.description.like(f'%{q}%')
            ))
    return items.order_by(Item.item_id.asc()).offset(offset).limit(limit).all()


def get_item_by_id(db: Session, item_id: int) -> Union[Item, None]:
    """
    Get item by id
    :param db:
    :param item_id:
    :return:
    """
    item = db.get(Item, item_id)
    if item:
        return item
    else:
        return None


def create_item(db: Session, item: ItemCreateSchema) -> Item:
    """
    Create new item
    :param db:
    :param item:
    :return:
    """
    new_item = Item(**item.dict(exclude_unset=True))
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def update_item(db: Session, item_id: int, item: ItemUpdateSchema) -> Union[Item, None]:
    """
    Update item
    :param db:
    :param item_id:
    :param item:
    :return:
    """
    existing_item = db.get(Item, item_id)
    if existing_item is None:
        return None
    else:
        for var, value in item.dict(exclude_unset=False).items():
            setattr(existing_item, var, value)
        db.commit()
        return existing_item


def disable_item(db: Session, item_id: int) -> Union[None, bool]:
    """
    Disable item by id
    :param db:
    :param item_id:
    :return:
    """
    item = db.get(Item, item_id)
    if item is None:
        return None
    else:
        try:
            item.disabled = True
            db.commit()
            return True
        except:
            # todo: need to log exception in disable_item
            return False
