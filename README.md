# Weather Forecasting API - Project Report

## Overview
This project implements a complete weather forecasting system using the [Meteomatics Weather API](https://www.meteomatics.com/en/weather-api/API). It retrieves 7-day forecasts for three selected cities and stores the results in a relational database. A RESTful API built with FastAPI provides access to this data via various endpoints.

## Process Summary
- Used Python to fetch weather forecasts for Athens, London, and Berlin.
- Queried hourly data over a 7-day range for multiple meteorological parameters.
- Parsed and normalized the JSON response using pandas.
- Stored the processed data in a SQLite database.
- Created a FastAPI application that exposes the following endpoints:
  - `/locations`: List all unique cities in the database.
  - `/forecasts`: Show latest forecast of each day (at 23:00) per city.
  - `/average_temperature`: Compute the average temperature of the last 3 hourly records per day per city.
  - `/top-locations`: Show the top N cities for each metric, with N provided as a query parameter.

## Key Decisions
- Chose SQLite for simplicity, portability, and easy file-based setup.
- Used pandas to handle all data transformations efficiently.
- FastAPI was chosen for its performance and ease of creating modern APIs.

## Challenges & Solutions
- **Datetime handling**: Had to carefully format and filter timestamps to ensure daily aggregations (e.g., 23:00 selection) were accurate.
- **Top-N logic**: Used SQL window functions (`ROW_NUMBER()`) to isolate top metrics per city, then rank them across all cities.

## Tools & Technologies
- **Language**: Python 3.10+
- **Data Fetching**: `requests`
- **Data Processing**: `pandas`
- **Database**: SQLite (`sqlalchemy`, `sqlite3`)
- **API Framework**: FastAPI

## Deliverables
- Source code (Python scripts)
- CSV export of the weather forecasts
- SQLite database file (`weather.db`)
- This project report in Markdown format

## Deployment
- The API is deployed and publicly accessible at: [https://weatherforecastapi-cyih.onrender.com/docs](https://weatherforecastapi-cyih.onrender.com/docs)
- It is ready for deployment to cloud services (e.g., AWS EC2, GCP App Engine).
- A `requirements.txt` file is included to simplify dependency installation.

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
3. Open your browser to: `http://127.0.0.1:8000/docs` to explore the API.

