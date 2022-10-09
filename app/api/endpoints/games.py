"""
Games routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.game import (
    GameSchema, GameCreateSchema, GameUpdateSchema, JoinRequestCreateSchema,
    JoinRequestSchema
)
from app.api.dependencies import get_db, get_current_user
from app.crud import game as crud
from app.crud import (
    CharacterUnavailable
)
from app.models.user import User
from app.api.endpoints import game_errors as error_details


router = APIRouter()


@router.get('/', response_model=list[GameSchema])
def read_all(db: Session = Depends(get_db)):
    """Read games"""
    return crud.get_games(db)


@router.get('/{game_id}', response_model=GameSchema)
def read_one(game_id: int,
             db: Session = Depends(get_db)):
    """Get game by id"""
    game = crud.get_game_by_id(game_id=game_id, db=db)
    if game is None:
        raise HTTPException(status_code=404)
    else:
        return game


@router.put('/{game_id}', response_model=GameSchema)
def update(game_id: int,
           game: GameUpdateSchema,
           current_user: User = Depends(get_current_user),
           db: Session = Depends(get_db)):
    """Update game"""
    # check if user has rights to modify the game
    if not current_user.is_gm(game_id):
        raise HTTPException(status_code=403, detail=error_details.USER_IS_NOT_GM)
    else:
        game = crud.update_game(db, game_id, game)
        if game is None:
            raise HTTPException(status_code=404)
        else:
            return game


@router.post('/', response_model=GameSchema)
def create(game: GameCreateSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create new game"""
    return crud.create_game(db=db, game=game, game_master_id=current_user.user_id)


@router.delete('/{game_id}')
def delete(game_id: int,
           current_user: User = Depends(get_current_user),
           db: Session = Depends(get_db)):
    """Delete game"""
    if not current_user.is_gm(game_id):
        raise HTTPException(status_code=403, detail=error_details.USER_IS_NOT_GM)
    response = crud.disable_game(db, game_id)
    if response is None:
        raise HTTPException(status_code=404)


@router.post('/{game_id}/join', response_model=JoinRequestSchema)
def create_join_request(
        game_id: int,
        join_request: JoinRequestCreateSchema,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    """
    Create new join request
    """
    # check if the user is the owner of the character
    if not current_user.owns_character(join_request.character_id):
        raise HTTPException(status_code=403, detail='No characters with provided id found')
    else:
        try:
            return crud.create_join_request(db, game_id, join_request)
        except CharacterUnavailable:
            raise HTTPException(status_code=400, detail=error_details.CHARACTER_ALREADY_USED)


@router.get('/{game_id}/join_requests', response_model=list[JoinRequestSchema])
def get_join_requests(
        game_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # check if the user is GM
    if not current_user.is_gm(game_id):
        raise HTTPException(status_code=403, detail=error_details.USER_IS_NOT_GM)
    else:
        return crud.get_join_requests(db, game_id)


@router.get('/{game_id}/join_requests/{request_id}/accept')
def accept_join_request(
        game_id: int,
        request_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Accept join request"""
    if not current_user.is_gm(game_id):
        raise HTTPException(status_code=403, detail=error_details.USER_IS_NOT_GM)
    else:
        crud.join_request_accept(db, request_id)


@router.get('/{game_id}/join_requests/{request_id}/decline')
def decline_join_request(
        game_id: int,
        request_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Decline join request"""
    if not current_user.is_gm(game_id):
        raise HTTPException(status_code=403, detail=error_details.USER_IS_NOT_GM)
    else:
        crud.join_request_decline(db, request_id)
