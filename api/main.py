from fastapi import Depends, FastAPI, HTTPException, Query
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


@app.get("/v1/players/{player_id}", response_model=schemas.Player)
def read_player(player_id: str, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player


@app.get("/v1/players/", response_model=schemas.Players)
def read_players(
    skip: int = Query(
        0, title="Skip records", description="Pagination offset. Number of records to be skiped"
    ),
    limit: int = Query(
        200, title="Records limit", description="Number of records per response", gt=0, le=200
    ),
    db: Session = Depends(get_db),
):
    players = crud.get_players(db, skip=skip, limit=limit)
    total_players = crud.get_players_count(db)

    if total_players - skip <= limit:
        has_more = False
    else:
        has_more = True

    return {"metadata": {"has_more": has_more, "offset": skip}, "body": players}
