"""
Character model class
"""

from sqlalchemy import Integer, String, Column, ForeignKey, \
    Boolean, Text, UniqueConstraint, PrimaryKeyConstraint, Index, DateTime
from sqlalchemy.orm import relationship, validates
from datetime import datetime

from app.database import Base
from app.models.refs import game_character
from app.core.operations.utils import CharacterAbilities


class Character(Base):

    __tablename__ = 'characters'

    character_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    biography = Column(String(255), default=None)
    disabled = Column(Boolean, default=False)
    user_owner_id = Column(Integer, ForeignKey('users.user_id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='characters')
    games = relationship('Game', secondary=game_character, back_populates='characters')

    def __init__(self,
                 name: str,
                 user_owner_id: int,
                 biography: str = None,
                 disabled: bool = False):
        self.name = name
        self.user_owner_id = user_owner_id
        self.biography = biography
        self.disabled = disabled
        self.abilities = None

    def load(self):
        self.abilities = CharacterAbilities(self.character_id)
