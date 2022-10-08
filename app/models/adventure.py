"""
Adventure model class
"""

from sqlalchemy import Integer, String, Column, ForeignKey, \
    Boolean, Text, UniqueConstraint, PrimaryKeyConstraint, Index, DateTime
from sqlalchemy.orm import relationship, validates
from datetime import datetime

from app.database import Base


class Adventure(Base):

    __tablename__ = 'adventures'

    aid = Column(Integer, primary_key=True)
    adventure_id = Column(Integer, default=None, index=True)
    name = Column(String(255), nullable=False)
    plot = Column(Text, default=None)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def is_locked(self):
        return False
