"""
Adventure schema
"""

from typing import Optional
import datetime
from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: int
    reusable: Optional[bool] = False
    weight: Optional[float] = 0
    cost: Optional[int] = 0
    disabled: bool = False


class ItemCreateSchema(ItemBase):
    pass


class ItemUpdateSchema(ItemBase):
    pass


class ItemSchema(ItemBase):
    item_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
