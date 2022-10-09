from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database.init_database import init_database
from app.api import api_router


init_database()

app = FastAPI(
    title='Dragonroll Gameserver API',
    version='0.0.1'
)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get('/info')
async def root():
    return {
        'app_name': settings.app_name,
        'sqlalchemy_uri': settings.db_uri
    }
