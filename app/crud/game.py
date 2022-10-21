"""
CRUD operations for Games
"""

from typing import Union
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.game import Game, GameJoinRequest
from app.models.character import Character
from app.schemas.game import GameCreateSchema, GameUpdateSchema, JoinRequestCreateSchema
from app.crud import (
    GameNotFound,
    JoinRequestNotFound,
    CharacterNotFound,
    CharacterUnavailable
)


def get_games(db: Session,
              owner_id: int = None,
              offset: int = 0,
              limit: int = 100) -> Union[list[Game], list]:
    """
    Get list of games from database
    :param db:
    :param owner_id: filter by owner id
    :param offset:
    :param limit:
    :return:
    """
    games = db.query(Game)
    if owner_id:
        games = games.filter(Game.owner_id == owner_id)
    return games.order_by(Game.game_id.asc()).offset(offset).limit(limit).all()


def get_game_by_id(db: Session, game_id: int) -> Union[Game, None]:
    """
    Get game by id
    :param db:
    :param game_id:
    :return:
    """
    game = db.get(Game, game_id)
    if game:
        return game
    else:
        return None


def create_game(db: Session, game: GameCreateSchema, game_master_id: int) -> Game:
    """
    Create new game
    :param db:
    :param game:
    :param game_master_id: the user who created the game
    :return:
    """
    new_game = Game(game_master_id=game_master_id, **game.dict(exclude_unset=True))
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game


def update_game(db: Session, game_id: int, game: GameUpdateSchema) -> Union[Game, None]:
    """
    Update game
    :param db:
    :param game_id:
    :param game:
    :return:
    """
    existing_game = db.get(Game, game_id)
    if existing_game is None:
        return None
    else:
        for var, value in game.dict(exclude_unset=False).items():
            setattr(existing_game, var, value)
        db.commit()
        return existing_game


def disable_game(db: Session, game_id: int) -> Union[None, bool]:
    """
    Disable game by id
    :param db:
    :param game_id:
    :return:
    """
    game = db.get(Game, game_id)
    if game is None:
        return None
    else:
        try:
            game.disabled = True
            db.commit()
            return True
        except:
            # todo: need to log exception in disable_game
            return False


def get_join_requests(db: Session, game_id: int, status_code: Union[int, list] = 1) -> list[GameJoinRequest]:
    """
    Get list of join requests for specified game
    :param db:
    :param game_id:
    :param status_code: can be a single status or list of statuses
    :return:
    """
    if isinstance(status_code, int):
        status_code = [status_code]
    return db.query(GameJoinRequest).filter(and_(
        GameJoinRequest.game_id == game_id),
        GameJoinRequest.status_code.in_(status_code)
    ).all()


def create_join_request(db: Session, game_id: int, join_request: JoinRequestCreateSchema) -> GameJoinRequest:
    """
    Create new join request
    :param db:
    :param game_id:
    :param join_request:
    :return:
    """
    new_request = GameJoinRequest(game_id=game_id, **join_request.dict(exclude_unset=True))
    db.add(new_request)
    db.commit()
    return new_request


def join_request_accept(db: Session, request_id: int):
    """
    Accept join request and add character to game
    :param db:
    :param request_id:
    :return:
    """
    join_request = db.get(GameJoinRequest, request_id)
    if join_request is None:
        raise JoinRequestNotFound

    # check if the game still exists
    game = db.get(Game, join_request.game_id)
    if game is None:
        raise GameNotFound

    # check if the character with specified id still exists
    character = db.get(Character, join_request.character_id)
    if character is None:
        raise CharacterNotFound
    if character.games:
        raise CharacterUnavailable

    game.characters.append(character)
    # set status_code as accepted
    join_request.status_code = 2
    db.commit()


def join_request_decline(db: Session, request_id: int):
    """
    Update join request with declined status
    :param db:
    :param request_id:
    :return:
    """
    join_request = db.get(GameJoinRequest, request_id)
    if join_request is None:
        raise JoinRequestNotFound
    # set status code as declined
    join_request.status_code = 3
    db.commit()
