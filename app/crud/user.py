"""
CRUD operations for Users
"""

from typing import Union
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.user import User
from app.schemas.user import UserCreateSchema, UserUpdateSchema


class UsernameNotUnique(Exception):
    pass


def get_users(db: Session,
              q: str = None,
              offset: int = 0,
              limit: int = 100) -> Union[list[User], list]:
    """
    Get list of users from database
    :param db:
    :param q: search filter query
    :param offset:
    :param limit:
    :return:
    """
    users = db.query(User)
    if q:
        users = users.filter(
            or_(
                User.username.like(f'%{q}%'),
                User.nickname.like(f'%{q}%')
            ))
    return users.order_by(User.user_id.asc()).offset(offset).limit(limit).all()


def get_user_by_id(db: Session, user_id: int) -> Union[User, None]:
    """
    Get user by id
    :param db:
    :param user_id:
    :return:
    """
    user = db.get(User, user_id)
    if user:
        return user
    else:
        return None


def get_user_by_name(db: Session, username: str) -> Union[User, None]:
    """
    Get user by username. Full match
    :param db:
    :param username:
    :return:
    """
    user = db.query(User).filter(User.username == username).first()
    if user:
        return user
    else:
        return None


def create_user(db: Session, user: UserCreateSchema) -> User:
    """
    Create new user
    :param db:
    :param user:
    :return:
    """
    # check if username is unique
    if db.query(User).filter(User.username == user.username).first() is not None:
        raise UsernameNotUnique
    else:
        new_user = User(**user.dict(exclude_unset=True))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


def update_user(db: Session, user_id: int, user: UserUpdateSchema) -> Union[User, None]:
    """
    Update user
    :param db:
    :param user_id:
    :param user:
    :return:
    """
    existing_user = db.get(User, user_id)
    if existing_user is None:
        return None
    else:
        for var, value in user.dict(exclude_unset=False).items():
            setattr(existing_user, var, value)
        db.commit()
        return existing_user


def disable_user(db: Session, user_id: int) -> Union[None, bool]:
    """
    Disable user by id
    :param db:
    :param user_id:
    :return:
    """
    user = db.get(User, user_id)
    if user is None:
        return None
    else:
        try:
            user.disabled = True
            db.commit()
            return True
        except:
            # todo: need to log exception in disable_item
            return False
