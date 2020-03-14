from sqlalchemy import Column, Date, ForeignKey, Integer, Interval, String

from .database import Base


class Player(Base):
    __tablename__ = "players"

    player_id = Column(String, primary_key=True, index=True)
    player_name = Column(String, index=True)
    email = Column(String, index=True)
    country = Column(String)
    last_login = Column(Date)


class Match(Base):
    __tablename__ = "matches"

    match_id = Column(String, primary_key=True, index=True)
    match_type = Column(String)
    player_1 = Column(String, ForeignKey("players.player_id"))
    player_2 = Column(String, ForeignKey("players.player_id"))
    match_date = Column(Date)
    match_duration = Column(Interval)


class Goal(Base):
    __tablename__ = "goals"

    goal_id = Column(Integer, primary_key=True)
    match_id = Column(String, ForeignKey("matches.match_id"))
    goal_timestamp = Column(Interval)
    player_id = Column(String, ForeignKey("players.player_id"))
