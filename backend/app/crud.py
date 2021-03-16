from datetime import date
from typing import Any, Dict, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app import models, schemas


def get_city_land_temperatures_in_date_range(
    db: Session,
    date_from: date,
    date_to: date,
    sort_order: Optional[schemas.SortOrder],
    limit: int = 100,
):
    sort_key = (
        models.LandTemperatures.average_temperature.asc()
        if sort_order == schemas.SortOrder.asc
        else models.LandTemperatures.average_temperature.desc()
    )
    return (
        db.query(models.LandTemperatures)
        .filter(
            and_(
                models.LandTemperatures.date >= date_from,
                models.LandTemperatures.date <= date_to,
                models.LandTemperatures.average_temperature.isnot(None)
            )
        )
        .order_by(sort_key)
        .limit(limit)
        .all()
    )


def get_city_land_temperatures_record_by_city_and_date(db: Session, record_date: date, city: str):
    return (
        db.query(models.LandTemperatures)
        .filter(
            and_(
                models.LandTemperatures.date == record_date,
                models.LandTemperatures.city == city,
            )
        )
        .first()
    )


def create_city_land_temperature(
    db: Session, city_land_temperature: schemas.LandTemperaturesCreate
):
    city_land_temperature_new = models.LandTemperatures(**city_land_temperature.dict())
    db.add(city_land_temperature_new)
    db.commit()
    db.refresh(city_land_temperature_new)
    return city_land_temperature_new


def update_city_land_temperatures(
    db: Session,
    db_obj: models.LandTemperatures,
    obj_in: Union[schemas.LandTemperaturesUpdate, Dict[str, Any]],
) -> models.LandTemperatures:
    obj_data = jsonable_encoder(db_obj)
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()
