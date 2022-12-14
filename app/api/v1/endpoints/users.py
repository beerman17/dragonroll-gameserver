"""
Users routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserSchema, UserCreateSchema, UserUpdateSchema
from app.api.v1.dependencies import get_db, get_current_user
from app.crud import user as crud
from app.api.v1.endpoints import user_errors as error_details
from app.models.user import User


router = APIRouter()


@router.get('/', response_model=list[UserSchema])
def read_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Read users"""
    return crud.get_users(db)


@router.get('/me')
def get_current_user_info(current_user=Depends(get_current_user)):
    """Get current user info"""
    # return user's data
    pass
    # return created games
    pass
    # return list of join requests
    pass
    # return list of characters
    pass
    # user = current_user
    # # user = None
    # if user is None:
    #     raise HTTPException(status_code=404)
    # else:
    #     return user
    return


@router.get('/{user_id}', response_model=UserSchema)
def read_one(user_id: int,
             db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    """Get user by id"""
    if not current_user.user_id == user_id:
        raise HTTPException(status_code=403, detail=error_details.USER_NOT_AUTHORIZED)
    user = crud.get_user_by_id(user_id=user_id, db=db)
    if user is None:
        raise HTTPException(status_code=404)
    else:
        return user


@router.put('/{user_id}', response_model=UserSchema)
def update(user_id: int, user: UserUpdateSchema,
           db: Session = Depends(get_db),
           current_user: User = Depends(get_current_user)):
    """Update user"""
    if not current_user.user_id == user_id:
        raise HTTPException(status_code=403, detail=error_details.USER_NOT_AUTHORIZED)
    user = crud.update_user(db, user_id, user)
    if user is None:
        raise HTTPException(status_code=404)
    else:
        return user


@router.post('/', response_model=UserSchema, status_code=201)
def create(user: UserCreateSchema, db: Session = Depends(get_db)):
    """Create new user"""
    try:
        return crud.create_user(db, user)
    except crud.UsernameNotUnique:
        raise HTTPException(status_code=400, detail=error_details.USERNAME_IS_NOT_UNIQUE)


@router.delete('/{user_id}')
def delete(user_id: int,
           current_user: User = Depends(get_current_user),
           db: Session = Depends(get_db)):
    """Delete user"""
    if not current_user.user_id == user_id:
        raise HTTPException(status_code=403, detail=error_details.USER_NOT_AUTHORIZED)
    response = crud.disable_user(db, user_id)
    if response is None:
        raise HTTPException(status_code=404)
