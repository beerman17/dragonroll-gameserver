"""
User model class
"""

from sqlalchemy import Integer, String, Column, ForeignKey, \
    Boolean, Text, UniqueConstraint, PrimaryKeyConstraint, Index, DateTime
from sqlalchemy.orm import relationship, validates
from datetime import datetime

from app.database import Base
from app.models.game import Game
from app.models.character import Character


class User(Base):

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    # email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), default=None)
    nickname = Column(String(255), default=None)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    games = relationship('Game', back_populates='game_master')
    characters = relationship('Character', back_populates='user')
    join_requests = relationship('GameJoinRequest', back_populates='user')

    def is_gm(self, game_id: int) -> bool:
        """
        Returns True if the user owns the game
        :param game_id:
        :return:
        """
        if game_id in [g.game_id for g in self.games]:
            return True
        else:
            return False

    def owns_character(self, character_id: int) -> bool:
        """
        Check if the user owns the character with specified id
        :param character_id:
        :return:
        """
        if character_id in [char.character_id for char in self.characters]:
            return True
        else:
            return False
