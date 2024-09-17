import pandas as pd
from pathlib import Path
from datetime import datetime
from database import engine, Base, get_db
from models import SolarPlantData
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import math
from typing import Optional

from utils import setup_logger

app = FastAPI()

# Initialize the database and create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Setup logging
log_directory = Path("logs")
logger = setup_logger(log_directory)


def clean_and_store_data(db: Session, csv_file: str):
    """
    Cleans the data from the CSV file and stores it in the PostgreSQL database.
    :param db: Database session
    :param csv_file: Path to the CSV file
    """
    logger.info(f"Starting data cleaning and storage from file: {csv_file}")

    # Load the CSV data
    try:
        data = pd.read_csv(csv_file)
        logger.info("CSV data loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading CSV file: {e}")
        raise HTTPException(status_code=500, detail="Error loading CSV file.")

    # Clean the data
    data['TIMESTAMP'] = pd.to_datetime(data['TIMESTAMP'], errors='coerce')
    data = data.dropna(subset=['TIMESTAMP', 'ID'])

    # Rename columns
    data.rename(columns={
        'TEMP': 'Temperature_C',
        'HUMIDITY': 'Humidity_Percent',
        'TOTAL_CLOUD_COVER': 'Cloud_Cover_Percent',
        'DEW_POINT': 'Dew_Point_C',
        'GLOBAL_RADIATION': 'Global_Radiation_W_m2',
    }, inplace=True)

    # Convert cleaned rows to database entries and insert into the database
    try:
        for _, row in data.iterrows():
            db_entry = SolarPlantData(
                temperature_c=row['Temperature_C'],
                humidity_percent=row['Humidity_Percent'],
                cloud_cover_percent=row['Cloud_Cover_Percent'],
                dew_point_c=row['Dew_Point_C'],
                global_radiation_w_m2=row['Global_Radiation_W_m2'],
                avg_wind_speed=row['AVG_WIND_SPEED'],
                avg_wind_direction=row['AVG_WIND_DIRECTION'],
                timestamp=row['TIMESTAMP']
            )
            db.add(db_entry)
        db.commit()
        logger.info("Data cleaned and stored successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error storing data into the database: {e}")
        raise HTTPException(status_code=500, detail="Error storing data into the database.")

# Endpoint to load and clean data from the CSV and store it in the database
@app.post("/load-data")
def load_data(db: Session = Depends(get_db)):
    """
    Endpoint to load, clean, and store data into the PostgreSQL database.
    :param db: Database session
    """
    logger.info("Received request to load data.")
    csv_file_path = 'data/dataset.csv'  # The path to the CSV file
    clean_and_store_data(db, csv_file_path)
    return {"message": "Data cleaned and loaded into the database successfully"}

# Example endpoint to get all data from the database
def sanitize_data(data):
    """Convert NaN, inf, -inf to None (which is JSON compliant)."""
    sanitized_data = []
    for item in data:
        sanitized_item = {}
        for key, value in item.items():
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                sanitized_item[key] = None  # Convert invalid floats to None
            else:
                sanitized_item[key] = value
        sanitized_data.append(sanitized_item)
    return sanitized_data

# Fetch all data from the database
@app.get("/data")
def get_filtered_data(
        db: Session = Depends(get_db),
        id: Optional[int] = None,
        start_timestamp: Optional[str] = Query(None, description="Start timestamp (YYYY-MM-DD format)"),
        end_timestamp: Optional[str] = Query(None, description="End timestamp (YYYY-MM-DD format)")
):
    logger.info("Received request to fetch data with filters.")

    # Build the query dynamically based on filters
    query = db.query(SolarPlantData)

    if id is not None:
        query = query.filter(SolarPlantData.id == id)
        logger.info(f"Filtering by ID: {id}")

    if start_timestamp:
        try:
            start_timestamp = datetime.strptime(start_timestamp, "%Y-%m-%d")
            query = query.filter(SolarPlantData.timestamp >= start_timestamp)
            logger.info(f"Filtering data from start timestamp: {start_timestamp}")
        except ValueError:
            logger.error("Invalid start_timestamp format. Use YYYY-MM-DD.")
            raise HTTPException(status_code=400, detail="Invalid start_timestamp format. Use YYYY-MM-DD.")

    if end_timestamp:
        try:
            end_timestamp = datetime.strptime(end_timestamp, "%Y-%m-%d")
            query = query.filter(SolarPlantData.timestamp <= end_timestamp)
            logger.info(f"Filtering data until end timestamp: {end_timestamp}")
        except ValueError:
            logger.error("Invalid end_timestamp format. Use YYYY-MM-DD.")
            raise HTTPException(status_code=400, detail="Invalid end_timestamp format. Use YYYY-MM-DD.")

    # Execute the query and retrieve results
    solar_plant_data = query.all()

    if not solar_plant_data:
        logger.warning("No data found for the given filters.")
        raise HTTPException(status_code=404, detail="No data found for the given filters")

    # Convert SQLAlchemy objects to dictionary and sanitize data
    data = [item.__dict__ for item in solar_plant_data]
    for item in data:
        item.pop("_sa_instance_state", None)

    sanitized_data = sanitize_data(data)

    logger.info("Data fetched and sanitized successfully.")
    return sanitized_data
