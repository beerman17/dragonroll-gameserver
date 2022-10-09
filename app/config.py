"""
Dragonroll Gameserver configuration
"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'Dragonroll Gameserver [Dev]'
    db_uri: str
    dev_mode: bool = True
    drop_db: bool = False


settings = Settings()


