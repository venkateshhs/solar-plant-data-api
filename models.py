

from sqlalchemy import Column, Integer, Float, String, DateTime

from database import Base


class SolarPlantData(Base):
    __tablename__ = "solar_plant_data"

    id = Column(Integer, primary_key=True, index=True)
    temperature_c = Column(Float)
    humidity_percent = Column(Float)
    cloud_cover_percent = Column(Float)
    dew_point_c = Column(Float)
    global_radiation_w_m2 = Column(Float)
    avg_wind_speed = Column(Float)
    avg_wind_direction = Column(Float)
    timestamp = Column(DateTime)
