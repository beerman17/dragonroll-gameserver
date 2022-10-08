"""
Reference tables
"""

from sqlalchemy import Integer, String, Column, ForeignKey, \
    Boolean, Text, UniqueConstraint, PrimaryKeyConstraint, Index, DateTime, Table
from sqlalchemy.orm import relationship, validates
from datetime import datetime

from app.database import Base


game_character = Table('games_characters_ref',
                       Base.metadata,
                       Column('id', Integer, primary_key=True),
                       Column('game_id', Integer, ForeignKey('games.game_id')),
                       Column('character_id', Integer, ForeignKey('characters.character_id'))
                       )

