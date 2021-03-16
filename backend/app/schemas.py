from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class LandTemperaturesBase(BaseModel):
    date: date
    city: str


class LandTemperaturesCreate(LandTemperaturesBase):
    country: Optional[str]
    average_temperature: Optional[float]
    average_temperature_uncertainty: Optional[float]
    latitude: Optional[str]
    longitude: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "date": "2020-11-01",
                "city": "Århus",
                "country": "Denmark",
                "average_temperature": 6.068,
                "average_temperature_uncertainty": 1.737,
                "latitude": "57.05N",
                "longitude": "10.33E"
                }
        }


class LandTemperaturesUpdate(LandTemperaturesBase):
    country: Optional[str]
    average_temperature: Optional[float]
    average_temperature_uncertainty: Optional[float]
    latitude: Optional[str]
    longitude: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "date": "2020-11-01",
                "city": "Århus",
                "country": "Denmark",
                "average_temperature": 6.068,
                "average_temperature_uncertainty": 1.737,
                "latitude": "57.05N",
                "longitude": "10.33E"
                }
        }


class LandTemperatures(LandTemperaturesBase):
    id: int
    country: str
    average_temperature: Optional[float]
    average_temperature_uncertainty: Optional[float]
    latitude: str
    longitude: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "date": "2020-11-01",
                "city": "Århus",
                "country": "Denmark",
                "average_temperature": 6.068,
                "average_temperature_uncertainty": 1.737,
                "latitude": "57.05N",
                "longitude": "10.33E"
                }
        }
