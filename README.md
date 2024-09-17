# Solar Plant Data Management API

This project provides an API for managing and accessing solar plant data, including features for data loading, filtering, and querying. The data is stored in a PostgreSQL database and served using FastAPI. The project leverages Docker for easy setup and deployment.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Logging](#logging)
- [Data Cleaning](#data-cleaning)
- [Future Improvements](#future-improvements)

## Project Overview

The goal of this project is to develop a REST API for handling solar plant data. The API allows users to load, clean, and store solar plant data from CSV files into a PostgreSQL database. Additionally, it offers functionality to filter and retrieve the stored data based on various parameters such as ID and timestamp ranges.

This solution is designed to be scalable and easy to deploy using Docker, making it suitable for real-world scenarios in solar plant data management and analysis.

## Features
- **Data Cleaning & Ingestion**: Load and clean solar plant data from CSV files and store it in a PostgreSQL database.
- **Data Filtering**: Query data based on solar plant ID or date ranges.
- **REST API**: Provides endpoints to interact with the solar plant data using FastAPI.
- **Docker Integration**: Uses Docker and Docker Compose to run the application and PostgreSQL database in isolated containers.
- **Logging**: Logs system events and errors with timestamped log files.

## Technologies Used
- **FastAPI**: A modern, fast web framework for building APIs with Python.
- **SQLAlchemy**: Python SQL toolkit and Object-Relational Mapping (ORM) library for database interaction.
- **PostgreSQL**: A powerful, open-source object-relational database system.
- **Docker & Docker Compose**: Tools to create and manage containerized environments for the API and database.
- **Pandas**: Data manipulation and analysis library, used for cleaning the CSV data.
- **Uvicorn**: ASGI server to run the FastAPI application.

## Setup and Installation

### Prerequisites
- Docker and Docker Compose installed on your machine.
- Python 3.9 (if running locally without Docker).

### Steps to Run the Project

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/venkateshhs/solar-plant-data-api.git
    cd solar-plant-data-api
    ```

2. **Open command Prompt in the solar-plant-data-api repository**: create venv using
    ```bash
   python -m venv venv
    ```
   Activate virtual environment using
    On windows
    ```bash
   .\venv\Scripts\activate
    ```
    Install required packages
    ```bash
     pip install -r requirements.txt
   ```
    Keep docker running

3. **Run the Application Using Docker**:
    ```bash
    docker-compose up --build
    ```
   This will:
   - Start the PostgreSQL container.
   - Build and run the FastAPI web server on port 8000.
   
4. **Load Data into the Application**:
    ```bash
    curl -X POST http://127.0.0.1:8000/load-data
    ```
5. **Fetch Data from the Application**:
    ```bash
    curl http://127.0.0.1:8000/data
    ```
   
    To retrieve data filtered by ID, start timestamp, and end timestamp:
    ```bash
   curl "http://localhost:8000/data?id=5&start_timestamp=2021-07-01&end_timestamp=2021-07-31"
    ```
    To retrieve data filtered by ID only:
    ```bash
   curl  "http://localhost:8000/data?id=5"
    ```
   
Alternatively you can run all the request using POSTMAN or just any normal browser(Although for PUT request you need to either use curl or POSTMAN)
## Database Schema

The project stores solar plant data using the following database schema, defined in `models.py`:

| Column                  | Data Type | Description                                         |
|-------------------------|-----------|-----------------------------------------------------|
| id                      | Integer   | Primary key, unique identifier for each record.     |
| temperature_c            | Float     | Ambient temperature in Celsius.                    |
| humidity_percent         | Float     | Humidity as a percentage.                          |
| cloud_cover_percent      | Float     | Cloud cover as a percentage.                       |
| dew_point_c              | Float     | Dew point temperature in Celsius.                  |
| global_radiation_w_m2    | Float     | Global solar radiation in W/m².                    |
| avg_wind_speed           | Float     | Average wind speed in m/s.                         |
| avg_wind_direction       | Float     | Average wind direction in degrees.                 |
| timestamp                | DateTime  | Timestamp of the data entry.                       |

## API Endpoints

### 1. Load and Clean Data - POST `/load-data`

This endpoint reads a CSV file (`data/dataset.csv`), cleans the data, and loads it into the PostgreSQL database.

**Response**:  
Success: `{"message": "Data cleaned and loaded into the database successfully"}`

### 2. Get Filtered Data - GET `/data`

Fetches solar plant data from the database based on optional filters.

#### Query Parameters:
- `id` (optional): Filter data by solar plant record ID.
- `start_timestamp` (optional): Filter data after a specific timestamp (format: YYYY-MM-DD).
- `end_timestamp` (optional): Filter data before a specific timestamp (format: YYYY-MM-DD).

**Example Request**:
```bash
GET /data?id=5&start_timestamp=2023-01-01&end_timestamp=2023-02-01
```
**Response**: 
```bash
[
  {
    "id": 5,
    "temperature_c": 25.0,
    "humidity_percent": 80.5,
    "cloud_cover_percent": 45.0,
    "dew_point_c": 15.0,
    "global_radiation_w_m2": 350.0,
    "avg_wind_speed": 3.5,
    "avg_wind_direction": 270.0,
    "timestamp": "2023-01-15T10:00:00"
  }
]
```

## Logging

The application uses a logging mechanism to record all system events. Logs are generated and stored in a directory specified by the `log_directory` parameter in the `setup_logger()` function. Each log file is named based on the timestamp when the log was created, ensuring logs are maintained in chronological order.

### Log Structure

- **Log Directory**: A folder is created for logs.
- **Log File Name**: Follows the format `YYYY-MM-DD_HH-MM-SS.log`.
- **Log Format**: Each log entry contains:
  - Timestamp
  - Log level (INFO, ERROR, etc.)
  - Log message


## Data Cleaning

The data cleaning process involves several steps to ensure the data is ready for storage and further analysis:

1. **Timestamp Parsing**: The `TIMESTAMP` column is converted to a datetime format, ensuring that invalid or malformed timestamps are removed using `pd.to_datetime()`.
2. **Handling Missing Values**: Rows where the `TIMESTAMP` or `ID` columns are missing are dropped to avoid incomplete entries.
3. **Column Renaming**: The column names are renamed to be more descriptive and consistent. For example, `TEMP` is renamed to `Temperature_C`, and `GLOBAL_RADIATION` to `Global_Radiation_W_m2`.
4. **Data Type Casting**: Necessary conversions are performed to ensure that the values in each column are of the appropriate data type, such as floating point for numerical values.
5. **NaN and Infinite Value Handling**: Before saving data, any invalid numerical values (like NaN or infinite numbers) are cleaned and replaced with `None` to maintain data integrity and prevent database errors.

These cleaning steps ensure the data is consistent, reliable, and ready for querying and analysis.


## Future Improvements

1. **Improved Data Validation**: Add more robust data validation checks before loading data into the database to handle unexpected data formats or missing values more gracefully.
2. **Extended API Functionality**: Additional endpoints to update or delete specific records, or more advanced filtering based on multiple parameters.
3. **Authentication**: Introduce authentication and authorization to secure the API endpoints.

