# app/crud.py

from sqlalchemy.orm import Session

from models import SolarPlantData


def get_all_solar_plant_data(db: Session):
    return db.query(SolarPlantData).all()


def get_solar_plant_data_by_id(db: Session, id: int):
    return db.query(SolarPlantData).filter(SolarPlantData.id == id).first()
