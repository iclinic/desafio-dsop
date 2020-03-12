from datetime import date
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
