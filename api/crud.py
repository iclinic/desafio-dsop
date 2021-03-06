from sqlalchemy.orm import Session

from . import models


def get_player(db: Session, player_id: str):
    return db.query(models.Player).filter(models.Player.player_id == player_id).first()


def get_player_by_email(db: Session, email: str):
    return db.query(models.Player).filter(models.Player.email == email).first()


def get_players(db: Session, skip: int = 0, limit: int = 200):
    return db.query(models.Player).offset(skip).limit(limit).all()


def get_players_by_name(db: Session, name: str, skip: int = 0, limit: int = 200):
    return (
        db.query(models.Player)
        .filter(models.Player.player_name.ilike(f"%{name}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_players_count(db: Session):
    return db.query(models.Player).count()
