
from typing import Optional, Any
import datetime
from pydantic import BaseModel


# noinspection PyUnboundLocalVariable
# class CharacterAbilitiesScheme(BaseModel):
#     hp: Optional[int]
#     ac: Optional[int]
#     str: Optional[int]
#     dex: Optional[int]
#     con: Optional[int]
#     int: Optional[int]
#     cha: Optional[int]
#
#     class Config:
#         orm_mode: True


class CharacterBase(BaseModel):
    name: str
    biography: Optional[str]


class CharacterCreateSchema(CharacterBase):
    pass


class CharacterUpdateSchema(CharacterBase):
    disabled: Optional[bool]


class CharacterSchema(CharacterBase):
    character_id: int
    user_owner_id: int
    disabled: Optional[bool]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    # abilities: Optional[CharacterAbilitiesScheme]

    class Config:
        orm_mode = True


class CharacterPublicScheme(CharacterBase):
    character_id: int
    user_owner_id: int

    class Config:
        orm_mode = True

