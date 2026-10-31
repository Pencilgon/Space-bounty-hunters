from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import Base, engine, get_db
from app import models, schemas


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Space Bounty Hunters API")


@app.get("/api/criminals/", response_model=list[schemas.CriminalResponse])
def get_criminals(
    min_reward: float | None = None,
    max_reward: float | None = None,
    armed: bool | None = None,
    has_crew: bool | None = None,
    escape_master: bool | None = None,
    sort: str | None = Query(None, pattern="^-?reward$"),
    db: Session = Depends(get_db)
):
    query = db.query(models.WantedCriminal)

    if min_reward is not None:
        query = query.filter(models.WantedCriminal.reward >= min_reward)

    if max_reward is not None:
        query = query.filter(models.WantedCriminal.reward <= max_reward)

    if armed is not None:
        query = query.filter(models.WantedCriminal.armed == armed)

    if has_crew is not None:
        query = query.filter(models.WantedCriminal.has_crew == has_crew)

    if escape_master is not None:
        query = query.filter(
            models.WantedCriminal.escape_master == escape_master
        )

    if sort == "reward":
        query = query.order_by(models.WantedCriminal.reward)

    elif sort == "-reward":
        query = query.order_by(desc(models.WantedCriminal.reward))

    return query.all()


@app.get(
    "/api/criminals/{criminal_id}/",
    response_model=schemas.CriminalResponse
)
def get_criminal(criminal_id: int, db: Session = Depends(get_db)):

    criminal = db.query(models.WantedCriminal).filter(
        models.WantedCriminal.id == criminal_id
    ).first()

    if not criminal:
        raise HTTPException(status_code=404, detail="Criminal not found")

    return criminal






@app.get("/api/hunts/", response_model=list[schemas.HuntLogResponse])
def get_hunts(
    criminal_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.HuntLog)

    if criminal_id is not None:
        query = query.filter(
            models.HuntLog.criminal_id == criminal_id
        )

    return query.all()


@app.get("/api/hunts/{hunt_id}/", response_model=schemas.HuntLogResponse)
def get_hunt(hunt_id: int, db: Session = Depends(get_db)):

    hunt = db.query(models.HuntLog).filter(
        models.HuntLog.id == hunt_id
    ).first()

    if not hunt:
        raise HTTPException(status_code=404, detail="Hunt log not found")

    return hunt


@app.post(
    "/api/hunts/",
    response_model=schemas.HuntLogResponse,
    status_code=201
)
def create_hunt(
    hunt_data: schemas.HuntLogCreate,
    db: Session = Depends(get_db)
):

    criminal = db.query(models.WantedCriminal).filter(
        models.WantedCriminal.id == hunt_data.criminal_id
    ).first()

    if not criminal:
        raise HTTPException(status_code=404, detail="Criminal not found")

    new_hunt = models.HuntLog(
        criminal_id=hunt_data.criminal_id,
        success=hunt_data.success,
        notes=hunt_data.notes
    )

    db.add(new_hunt)
    db.commit()
    db.refresh(new_hunt)

    return new_hunt


@app.patch(
    "/api/hunts/{hunt_id}/",
    response_model=schemas.HuntLogResponse
)
def update_hunt(
    hunt_id: int,
    hunt_data: schemas.HuntLogUpdate,
    db: Session = Depends(get_db)
):

    hunt = db.query(models.HuntLog).filter(
        models.HuntLog.id == hunt_id
    ).first()

    if not hunt:
        raise HTTPException(status_code=404, detail="Hunt log not found")

    update_data = hunt_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(hunt, key, value)

    db.commit()
    db.refresh(hunt)

    return hunt


@app.delete("/api/hunts/{hunt_id}/", status_code=204)
def delete_hunt(hunt_id: int, db: Session = Depends(get_db)):

    hunt = db.query(models.HuntLog).filter(
        models.HuntLog.id == hunt_id
    ).first()

    if not hunt:
        raise HTTPException(status_code=404, detail="Hunt log not found")

    db.delete(hunt)
    db.commit()

    return None