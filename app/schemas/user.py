
from typing import Optional
import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    nickname: Optional[str]


class UserCreateSchema(UserBase):
    password: Optional[str]


class UserUpdateSchema(BaseModel):
    nickname: Optional[str]
    password: Optional[str]
    disabled: Optional[bool]


class UserSchema(UserBase):
    user_id: int
    disabled: Optional[bool]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class UserLobbySchema(BaseModel):
    pass
