"""
Gametable model class
"""

from sqlalchemy import Integer, String, Column, ForeignKey, \
    Boolean, Text, UniqueConstraint, PrimaryKeyConstraint, Index, DateTime, Table
from sqlalchemy.orm import relationship, validates
from datetime import datetime

from app.database import Base
from app.models.refs import game_character


class Game(Base):

    __tablename__ = 'games'

    game_id = Column(Integer, primary_key=True)
    game_master_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    game_state = Column(Boolean, default=True)
    disabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    characters = relationship('Character', secondary=game_character, back_populates='games')
    game_master = relationship('User', back_populates='games')


class GameJoinRequest(Base):
    """
    Status codes:
        1 - pending
        2 - accepted
        3 - declined
    """
    __tablename__ = 'games_join_requests'

    request_id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.game_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    character_id = Column(Integer, ForeignKey('characters.character_id'), nullable=False)
    message = Column(String(255), default=None)
    status_code = Column(Integer, default=1)

    user = relationship('User', back_populates='join_requests')
    character = relationship('Character')

    def __int__(self,
                game_id: int,
                character_id: int,
                message: str = None,
                status_code: int = 0):
        self.game_id = game_id
        self.character_id = character_id
        self.message = message
        self.status_code = status_code

    @property
    def status(self):
        codes = {
            1: 'pending',
            2: 'accepted',
            3: 'declined'
        }
        return codes[self.status_code]
