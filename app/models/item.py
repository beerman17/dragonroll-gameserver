"""
Item model class
"""

from sqlalchemy import Integer, String, Float, Column, ForeignKey, \
    Boolean, Text, UniqueConstraint, PrimaryKeyConstraint, Index, DateTime
from sqlalchemy.orm import relationship, validates
from datetime import datetime

from app.database import Base


"""
Item -> Ref-table <-> Character's Inventory
"""


class Item(Base):
    """
    Item possible types:
    1. gear
    2. weapon
    3. armor
    4. food
    5. goods
    6. clothing
    7. money
    """

    __tablename__ = 'items'

    item_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, default=None)
    type = Column(Integer, nullable=False)
    reusable = Column(Boolean, default=False)
    weight = Column(Float, default=0)
    # todo: need to thing about durability
    # durability = Column(Integer, default=0)
    cost = Column(Integer, default=0)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# class ItemFeatureUse(Base):
#
#     __tablename__ = 'items_features_use'
#     pass
#
#
# class ItemFeatureAttack(Base):
#     """
#     Weapon
#
#     class:
#         1 - simple
#         2 - martial
#         3 - exotic
#
#     encumbrance:
#         1 - light
#         2 - one-handed
#         3 - two-handed
#
#     size:
#         1 - small
#         2 - medium
#
#     type:
#         1 - bludgeoning
#         2 - piercing
#         3 - slashing
#
#     """
#
#     __tablename__ = 'items_features_attack'
#
#     pass
#
#
# class ItemFeatureConsume(Base):
#
#     __tablename__ = 'items_features_consume'
#
#     pass
#
#
# class ItemImpactEquip(Base):
#
#     __tablename__ = 'items_features_equip'
#
#     pass
