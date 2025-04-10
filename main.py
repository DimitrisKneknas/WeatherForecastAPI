from fastapi import FastAPI, Query
from sqlalchemy import create_engine, text
import pandas as pd
from typing import List, Dict

app = FastAPI()
engine = create_engine("sqlite:///weather.db")

@app.get("/")
def root():
    return {"message": "Weather Forecast API"}


@app.get("/locations")
def list_locations():
    query = "SELECT DISTINCT City FROM weather_forecast"
    df = pd.read_sql(query, engine)
    return df["City"].tolist()


@app.get("/forecasts")
def latest_forecasts():
    query = """
    SELECT City, DATE(Date) as DateOnly, Temperature, MaxTemp, MinTemp, Humidity, Pressure, 
           WindSpeed, WindDirection, WindGusts, Precipitation
    FROM weather_forecast
    WHERE strftime('%H:%M:%S', Date) = '23:00:00'
    ORDER BY Date
    """
    df = pd.read_sql(query, engine)
    # print(df)
    return df.to_dict(orient="records")


@app.get("/average_temperature")
def average_temperature():
    query = """
    SELECT City, Temperature, Date, DATE(Date) as DateOnly
    FROM weather_forecast
    ORDER BY City, Date DESC
    """
    df = pd.read_sql(query, engine)
    top3 = df.groupby(['City', 'DateOnly']).head(3)
    # print(top3)
    avg_temp = top3.groupby(['City', 'DateOnly'])['Temperature'].mean().reset_index()
    avg_temp = avg_temp.sort_values(by='DateOnly')
    # print(avg_temp)
    return avg_temp.to_dict(orient="records")


def get_top_locations_by_metric(metric: str, n: int, ascending: bool = False) -> List[Dict]:
    order = "ASC" if ascending else "DESC"
    query = text(f"""
    SELECT City, value FROM (
        SELECT City, "{metric}" as value,
               ROW_NUMBER() OVER (PARTITION BY City ORDER BY "{metric}" {order}) as rn
        FROM weather_forecast
        WHERE "{metric}" IS NOT NULL
    ) 
    WHERE rn = 1
    ORDER BY value {order}
    LIMIT :limit
    """)
    df = pd.read_sql(query, engine, params={"limit": n})
    return df.to_dict(orient="records")


@app.get("/top-locations")
def top_locations(n: int = Query(3, ge=1, le=3)):
    metrics = [ 
        "Temperature", "MaxTemp", "MinTemp", "Humidity", "Pressure", 
        "WindSpeed", "WindDirection", "WindGusts", "Precipitation"
    ]
    result = {}
    for metric in metrics:
        ascending = (metric == "MinTemp")
        result[metric] = get_top_locations_by_metric(metric, n, ascending=ascending)

    return result