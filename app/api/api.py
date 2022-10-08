from fastapi import APIRouter

from app.api.endpoints import adventures, characters, games, items, users


api_router = APIRouter()

# api_router.include_router(adventures.router, prefix='/adventures', tags=['adventures'])
# api_router.include_router(items.router, prefix='/items', tags=['items'])
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(characters.router, prefix='/character', tags=['character'])
api_router.include_router(games.router, prefix='/games', tags=['games'])
