import pymysql
from dbutils.pooled_db import PooledDB
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from .config import DB_HOST, DB_USER, DB_PASSWD, DB_NAME
from datetime import datetime
import pandas as pd
from .predictor import WeatherPredictor

pool = PooledDB(
    creator=pymysql,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWD,
    database=DB_NAME,
    maxconnections=1,
    blocking=True,
)

app_api = FastAPI()
router = APIRouter(prefix="/explan")


class BetterBaseModel(BaseModel):
    @classmethod
    def get_field_names(cls):
        return cls.model_fields.keys()

    def __init__(self, *args):
        field_names = self.get_field_names()
        kwargs = dict(zip(field_names, args))
        super().__init__(**kwargs)


class WeatherData(BetterBaseModel):
    ts: datetime
    location: str
    wind_speed: float
    wind_degree: float
    pressure: float
    temperature: float
    humidity: float
    cloud_percent: float
    rainfall: float
    weather: str


class TemperatureData(BetterBaseModel):
    ts: datetime
    location: str
    temperature: float


class HumidityData(BetterBaseModel):
    ts: datetime
    location: str
    humidity: float


class RainfallData(BetterBaseModel):
    ts: datetime
    location: str
    rainfall: float
    weather: str


@router.get("/locations")
async def get_locations() -> list[str]:
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT DISTINCT location FROM `weather_cleaned`
        """)
        result = [location[0] for location in cs.fetchall()]
    if not result:
        return HTTPException(404, "No location data found")
    return result


@router.get("/weather")
async def get_closest_time_weather(
    location: str, datetime: datetime = datetime.now()
) -> WeatherData:
    if not location:
        raise HTTPException(400, "Please specify a location")
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute(f"""
            SELECT ts, location, wind_sp, wind_deg,
            pressure, temperature, humidity,
            cloud_per, rain_amt, weather
            FROM `weather_cleaned`
            WHERE location = "{location}"
            ORDER BY ABS(TIMESTAMPDIFF(SECOND, ts, "{datetime.isoformat()}"))
            ASC LIMIT 1;
        """)
        result = cs.fetchone()
    if not result:
        raise HTTPException(404, "No weather data found")
    return WeatherData(*result)


@router.get("/weather/last")
async def get_last_days_weather(location: str, days: int = 1):
    if not location:
        raise HTTPException(400, "Please specify a location")
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute(f"""
            SELECT ts, location, wind_sp, wind_deg,
            pressure, temperature, humidity,
            cloud_per, rain_amt, weather
            FROM `weather_cleaned`
            WHERE location = "{location}"
            AND DATE(ts) >= DATE_SUB(NOW(), INTERVAL {days} DAY)
        """)
        result = [WeatherData(*data) for data in cs.fetchall()]
    if not result:
        return HTTPException(404, f"No weather data found in the last {days} day")
    return result


@router.get("/weather/aggregate")
async def get_aggregate_weather(location: str, days: int = 1):
    if not location:
        raise HTTPException(400, "Please specify a location")
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute(f"""
            SELECT DATE(ts) AS ts_agg, location, AVG(wind_sp), AVG(wind_deg),
            AVG(pressure), AVG(temperature), AVG(humidity),
            AVG(cloud_per), SUM(rain_amt), GROUP_CONCAT(DISTINCT weather)
            FROM `weather_cleaned`
            WHERE location = "{location}"
            AND DATE(ts) >= DATE_SUB(NOW(), INTERVAL {days} DAY)
            GROUP BY ts_agg
        """)
        result = [WeatherData(*data) for data in cs.fetchall()]
    if not result:
        return HTTPException(404, f"No weather data found in the last {days} day")
    return result


@router.get("/temperature/max")
async def get_max_temperature(location: str, days: int = 1):
    if not location:
        raise HTTPException(400, "Please specify a location")
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute(f"""
            SELECT ts, location, temperature
            FROM `weather_cleaned`
            WHERE location = "{location}"
            AND DATE(ts) >= DATE_SUB(NOW(), INTERVAL {days} DAY)
            ORDER BY temperature DESC, ts DESC
            LIMIT 1;
        """)
        result = cs.fetchone()
    if not result:
        raise HTTPException(404, f"No temperature data found in the last {days} days")
    return TemperatureData(*result)


@router.get("/temperature/min")
async def get_min_temperature(location: str, days: int = 1):
    if not location:
        raise HTTPException(400, "Please specify a location")
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute(f"""
            SELECT ts, location, temperature
            FROM `weather_cleaned`
            WHERE location = "{location}"
            AND DATE(ts) >= DATE_SUB(NOW(), INTERVAL {days} DAY)
            ORDER BY temperature ASC, ts DESC
            LIMIT 1;
        """)
        result = cs.fetchone()
    if not result:
        raise HTTPException(404, f"No temperature data found in the last {days} days")
    return TemperatureData(*result)


@router.get("/humidity/max")
async def get_max_humidity(location: str, days: int = 1):
    if not location:
        raise HTTPException(400, "Please specify a location")
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute(f"""
            SELECT ts, location, humidity
            FROM `weather_cleaned`
            WHERE location = "{location}"
            AND DATE(ts) >= DATE_SUB(NOW(), INTERVAL {days} DAY)
            ORDER BY humidity DESC, ts DESC
            LIMIT 1;
        """)
        result = cs.fetchone()
    if not result:
        raise HTTPException(404, f"No humidity data found in the last {days} days")
    return HumidityData(*result)


@router.get("/humidity/min")
async def get_min_humidity(location: str, days: int = 1):
    if not location:
        raise HTTPException(400, "Please specify a location")
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute(f"""
            SELECT ts, location, humidity
            FROM `weather_cleaned`
            WHERE location = "{location}"
            AND DATE(ts) >= DATE_SUB(NOW(), INTERVAL {days} DAY)
            ORDER BY humidity ASC, ts DESC
            LIMIT 1;
        """)
        result = cs.fetchone()
    if not result:
        raise HTTPException(404, f"No humidity data found in the last {days} days")
    return HumidityData(*result)


@router.get("/rainfall/max")
async def get_max_rainfall(location: str, days: int = 1):
    if not location:
        raise HTTPException(400, "Please specify a location")
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute(f"""
            SELECT ts, location, rain_amt, weather
            FROM `weather_cleaned`
            WHERE location = "{location}"
            AND DATE(ts) >= DATE_SUB(NOW(), INTERVAL {days} DAY)
            ORDER BY rain_amt DESC, ts DESC
            LIMIT 1;
        """)
        result = cs.fetchone()
    if not result:
        raise HTTPException(404, f"No rainfall data found in the last {days} days")
    return RainfallData(*result)


@router.get("/rainfall/min")
async def get_min_rainfall(location: str, days: int = 1):
    if not location:
        raise HTTPException(400, "Please specify a location")
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute(f"""
            SELECT ts, location, rain_amt, weather
            FROM `weather_cleaned`
            WHERE location = "{location}"
            AND DATE(ts) >= DATE_SUB(NOW(), INTERVAL {days} DAY)
            ORDER BY rain_amt ASC, ts DESC
            LIMIT 1;
        """)
        result = cs.fetchone()
    if not result:
        raise HTTPException(404, f"No rainfall data found in the last {days} days")
    return RainfallData(*result)


@router.get("/predict/temperature")
async def get_temperature_prediction(location: str, ts: str):
    try:
        date = datetime.strptime(ts, "%Y/%m/%d %H:%M")
    except (ValueError, TypeError):
        raise HTTPException(422, f"{ts} is not of format %y/%m/%d %H:%M")
    result = WeatherPredictor().forecast_temperature(ts, location)
    if not result:
        raise HTTPException(404, f"No predictor found for the location:{location}")
    for data in result:
        data["location"] = location
    return result


@router.get("/predict/humidity")
async def get_humidity_prediction(location: str, ts: str):
    try:
        date = datetime.strptime(ts, "%Y/%m/%d %H:%M")
    except (ValueError, TypeError):
        raise HTTPException(422, f"{ts} is not of format %y/%m/%d %H:%M")
    result = WeatherPredictor().forecast_humidity(ts, location)
    if not result:
        raise HTTPException(404, f"No predictor found for the location:{location}")
    for data in result:
        data["location"] = location
    return result


@router.get("/predict/pressure")
async def get_pressure_prediction(location: str, ts: str):
    try:
        date = datetime.strptime(ts, "%Y/%m/%d %H:%M")
    except (ValueError, TypeError):
        raise HTTPException(422, f"{ts} is not of format %y/%m/%d %H:%M")
    result = WeatherPredictor().forecast_pressure(ts, location)
    if not result:
        raise HTTPException(404, f"No predictor found for the location:{location}")
    for data in result:
        data["location"] = location
    return result


@router.get("/predict/rain")
async def get_rain_prediction(location, start, end):
    try:
        start_date = datetime.strptime(start, "%Y/%m/%d %H:%M")
        end_date = datetime.strptime(end, "%Y/%m/%d %H:%M")
    except (ValueError, TypeError):
        raise HTTPException(422, f"{start}, {end} is not of format %y/%m/%d %H:%M")
    if start_date > end_date:
        raise HTTPException(422, "starting date greater than ending date.")
    temp = pd.DataFrame(WeatherPredictor().forecast_temperature(end, location))
    humidity = pd.DataFrame(WeatherPredictor().forecast_humidity(end, location))
    pressure = pd.DataFrame(WeatherPredictor().forecast_pressure(end, location))
    ts = temp["ts"]
    weather_data = (
        temp.merge(humidity, on=["ts"], how="outer")
        .merge(pressure, on=["ts"], how="outer")
        .drop(columns=["ts"])
    )
    result = WeatherPredictor().forecast_rain(weather_data)
    for i in range(len(result)):
        result[i]["ts"] = ts.iloc[i]
        result[i]["location"] = location
    return result


app_api.include_router(router)
