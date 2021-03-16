from datetime import date
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import SessionLocal, engine

tables_initialized = False

app = FastAPI()


# Dependency
def get_db():
    global tables_initialized
    if not tables_initialized:
        models.Base.metadata.create_all(bind=engine)
        tables_initialized = True
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/city_land_temperatures/", response_model=List[schemas.LandTemperatures])
def read_city_land_temperatures(
    date_from: date,
    date_to: date,
    sort_order: schemas.SortOrder = schemas.SortOrder.asc,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    items = crud.get_city_land_temperatures_in_date_range(
        db, date_from=date_from, date_to=date_to, sort_order=sort_order, limit=limit
    )
    return items


@app.post("/city_land_temperatures/", response_model=schemas.LandTemperatures)
def create_city_land_temperature(
    city_land_temperature: schemas.LandTemperaturesCreate,
    db: Session = Depends(get_db),
):
    return crud.create_city_land_temperature(db, city_land_temperature=city_land_temperature)


@app.patch("/city_land_temperatures/", response_model=schemas.LandTemperatures)
def update_city_land_temperature(
    city_land_temperature: schemas.LandTemperaturesUpdate,
    db: Session = Depends(get_db),
):

    city_land_temperature_in_db = crud.get_city_land_temperatures_record_by_city_and_date(
        db, record_date=city_land_temperature.date, city=city_land_temperature.city
    )
    if city_land_temperature_in_db is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "no record in database for "
                f"{str(city_land_temperature.date), city_land_temperature.city}"),
        )
    return crud.update_city_land_temperatures(
        db=db, db_obj=city_land_temperature_in_db, obj_in=city_land_temperature
    )
