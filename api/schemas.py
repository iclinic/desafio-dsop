from datetime import date
from typing import List

from pydantic import BaseModel


class PlayerBase(BaseModel):
    player_name: str
    email: str


class Player(PlayerBase):
    player_id: str
    country: str
    last_login: date

    class Config:
        orm_mode = True


class Metadata(BaseModel):
    has_more: bool
    offset: int


class Players(BaseModel):
    metadata: Metadata
    body: List[Player]
