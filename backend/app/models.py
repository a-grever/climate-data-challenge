

from sqlalchemy import Column, String, Float, Date, Integer

from app.database import Base


class LandTemperatures(Base):
    __tablename__ = 'land_temperatures'

    id = Column(Integer, primary_key=True)
    date = Column(Date, index=True, nullable=False)
    average_temperature = Column(Float)
    average_temperature_uncertainty = Column(Float)
    city = Column(String)
    country = Column(String)
    latitude = Column(String)
    longitude = Column(String)
