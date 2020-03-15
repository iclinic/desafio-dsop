from datetime import date
from typing import List

from pydantic import BaseModel, Field


class PlayerBase(BaseModel):
    player_name: str = Field(..., title="Player name", description="Full name of the player.")
    email: str = Field(..., title="Email of the player", description="Registered email of the player.")


class Player(PlayerBase):
    player_id: str = Field(..., title="Player ID", description="Alphanumerical ID of the player.")
    country: str = Field(..., title="Country", description="Country of registration.")
    last_login: date = Field(..., title="Last player login", description="The last date this player logged on.")

    class Config:
        orm_mode = True


class Metadata(BaseModel):
    has_more: bool = Field(
        ..., title="More records", description="Indicates if there is more records to paginate.",
    )
    offset: int = Field(..., title="Records offset", description="Number of records skipped.")


class Players(BaseModel):
    metadata: Metadata
    body: List[Player]
