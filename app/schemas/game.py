from typing import Optional, Literal
import datetime
from pydantic import BaseModel

from .user import UserBase

'''
Game entity schemas
'''


class GameBase(BaseModel):
    pass


class GameCreateSchema(GameBase):
    pass


class GameUpdateSchema(GameBase):
    game_state: Optional[bool]


class GameSchema(GameBase):
    game_id: int
    game_master_id: int
    game_state: Optional[bool]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


'''
Join requests entity schemas
'''


class JoinRequestBaseSchema(BaseModel):
    user_id: int
    character_id: int
    message: Optional[str]


class JoinRequestCreateSchema(JoinRequestBaseSchema):
    pass


class JoinRequestUpdateSchema(JoinRequestBaseSchema):
    pass


class JoinRequestSchema(JoinRequestBaseSchema):
    request_id: int
    game_id: int
    status: Literal['pending', 'accepted', 'declined']

    class Config:
        orm_mode = True
