from fastapi import Depends, FastAPI, HTTPException, Path, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="iClinic - Desafio ProductOps", version="v1")
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/", response_class=FileResponse, include_in_schema=False)
async def home():
    return FileResponse("./static/home.html", status_code=200)


@app.get(
    "/v1/players/{player_id}",
    response_model=schemas.Player,
    summary="Get player by ID",
    description="Uses the player ID key to get player info.",
    response_description="A player object",
    tags=["players"],
)
def read_player(
    player_id: str = Path(..., title="Player ID", description="ID of the player"),
    db: Session = Depends(get_db),
):
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player


@app.get(
    "/v1/players/email/{email}",
    response_model=schemas.Player,
    summary="Get player by email",
    description="Uses the player's email to get info.",
    response_description="A player object",
    tags=["players"],
)
def read_player(
    email: str = Path(..., title="Email", description="Email of the player"),
    db: Session = Depends(get_db),
):
    db_player = crud.get_player_by_email(db, email=email)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player


@app.get(
    "/v1/players/",
    response_model=schemas.Players,
    summary="Get all players",
    description="Get all the players and paginates the records with an offset value",
    response_description="List of players",
    tags=["players"],
)
def read_players(
    skip: int = Query(
        0, title="Skip records", description="Pagination offset. Number of records to be skiped",
    ),
    limit: int = Query(
        200, title="Records limit", description="Number of records per response", gt=0, le=200,
    ),
    name: str = Query(
        None,
        title="Player name",
        description="Name or part of name to be matched against.",
        min_length=3,
        max_length=15,
    ),
    db: Session = Depends(get_db),
):
    if name:
        players = crud.get_players_by_name(db, name=name, skip=skip, limit=limit)
    else:
        players = crud.get_players(db, skip=skip, limit=limit)

    total_players = crud.get_players_count(db)
    if total_players - skip <= limit:
        has_more = False
    else:
        has_more = True

    return {"metadata": {"has_more": has_more, "offset": skip}, "body": players}
