"""
Adventure schema
"""

from typing import Optional
import datetime
from pydantic import BaseModel


class AdventureBase(BaseModel):
    name: str
    plot: Optional[str] = None


class AdventureCreateSchema(AdventureBase):
    pass


class AdventureUpdateSchema(AdventureBase):
    pass


class AdventureSchema(AdventureBase):
    adventure_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class AdventureInDBSchema(AdventureSchema):
    aid: int
    is_active: bool
    is_locked: bool
