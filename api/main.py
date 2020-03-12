from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/players/{player_id}", response_model=schemas.Player)
def read_player(player_id: str, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player


@app.get("/players/", response_model=schemas.Player)
def read_players(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    players = crud.get_players(db, skip=skip, limit=limit)
    return players
