import pymysql
from dbutils.pooled_db import PooledDB
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from .config import DB_HOST, DB_USER, DB_PASSWD, DB_NAME
from datetime import datetime
import pandas as pd
from .predictor import WeatherPredictor
from .advisor import EventAdvisor, HeatIndexCalculator

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


class EventWeatherData(BaseModel):
    weather: str
    ts: str
    location: str | None = ""
    temperature: float
    humidity: float


class EventWeatherDataList(BaseModel):
    data: list[EventWeatherData]


class HeatIndexData(BaseModel):
    temperature: float
    humidity: float
    ts: str | None = ""


class HeatIndexDataList(BaseModel):
    data: list[HeatIndexData]


class SensorData(BetterBaseModel):
    ts: datetime
    temperature: float
    humidity: float
    co: float


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
    location: str, date_time: str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
) -> WeatherData:
    try:
        date = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S")
    except (ValueError, TypeError):
        raise HTTPException(422, f"{date_time} is not of format %Y-%m-%dT%H:%M:%S")
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute(f"""
            SELECT ts, location, wind_sp, wind_deg,
            pressure, temperature, humidity,
            cloud_per, rain_amt, weather
            FROM `weather_cleaned`
            WHERE location = "{location}"
            ORDER BY ABS(TIMESTAMPDIFF(SECOND, ts, "{date.isoformat()}"))
            ASC LIMIT 1;
        """)
        result = cs.fetchone()
    if not result:
        raise HTTPException(404, "No weather data found")
    return WeatherData(*result)


@router.get("/weather/last")
async def get_last_days_weather(location: str, days: int = 1):
    if days < 0:
        raise HTTPException(422, f"Given days:{days} is not positive.")
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
        raise HTTPException(404, f"No weather data found in the last {days} day")
    return result


@router.get("/weather/aggregate")
async def get_aggregate_weather(location: str, days: int = 1):
    if days < 0:
        raise HTTPException(422, f"Given days:{days} is not positive.")
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
        raise HTTPException(404, f"No weather data found in the last {days} day")
    return result


@router.get("/temperature/max")
async def get_max_temperature(location: str, days: int = 1):
    if days < 0:
        raise HTTPException(422, f"Given days:{days} is not positive.")
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
    if days < 0:
        raise HTTPException(422, f"Given days:{days} is not positive.")
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
    if days < 0:
        raise HTTPException(422, f"Given days:{days} is not positive.")
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
    if days < 0:
        raise HTTPException(422, f"Given days:{days} is not positive.")
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
    if days < 0:
        raise HTTPException(422, f"Given days:{days} is not positive.")
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
    if days < 0:
        raise HTTPException(422, f"Given days:{days} is not positive.")
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
        date = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")
    except (ValueError, TypeError):
        raise HTTPException(422, f"{ts} is not of format %Y-%m-%dT%H:%M:%S")
    if date < datetime.now():
        raise HTTPException(400, "Cannot predict past dates.")
    location = location.replace(' ', '_')
    locations = WeatherPredictor(pool).get_valid_predictor_locations()
    if location not in locations:
        raise HTTPException(404,f"No predictor found for the location:{location}")
    result = WeatherPredictor(pool).forecast_temperature(ts, location)
    for data in result:
        data["location"] = location
    return result


@router.get("/predict/humidity")
async def get_humidity_prediction(location: str, ts: str):
    try:
        date = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")
    except (ValueError, TypeError):
        raise HTTPException(422, f"{ts} is not of format %Y-%m-%dT%H:%M:%S")
    if date < datetime.now():
        raise HTTPException(400, "Cannot predict past dates.")
    location = location.replace(' ', '_')
    locations = WeatherPredictor(pool).get_valid_predictor_locations()
    if location not in locations:
        raise HTTPException(404,
                            f"No predictor found for the location:{location}")
    result = WeatherPredictor(pool).forecast_humidity(ts, location)
    for data in result:
        data["location"] = location
    return result


@router.get("/predict/pressure")
async def get_pressure_prediction(location: str, ts: str):
    try:
        date = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")
    except (ValueError, TypeError):
        raise HTTPException(422, f"{ts} is not of format %Y-%m-%dT%H:%M:%S")
    if date < datetime.now():
        raise HTTPException(400, "Cannot predict past dates.")
    location = location.replace(' ', '_')
    locations = WeatherPredictor(pool).get_valid_predictor_locations()
    if location not in locations:
        raise HTTPException(404,
                            f"No predictor found for the location:{location}")
    result = WeatherPredictor(pool).forecast_pressure(ts, location)
    for data in result:
        data["location"] = location
    return result


@router.get("/predict/rain")
async def get_rain_prediction(location, start, end):
    try:
        start_date = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        end_date = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
    except (ValueError, TypeError):
        raise HTTPException(422, f"{start}, {end} is not of format %Y-%m-%dT%H:%M:%S")
    if start_date > end_date:
        raise HTTPException(422, "starting date greater than ending date.")
    if start_date < datetime.now() or end_date < datetime.now():
        raise HTTPException(400, "Cannot predict past dates.")
    location = location.replace(' ', '_')
    locations = WeatherPredictor(pool).get_valid_predictor_locations()
    if location not in locations:
        raise HTTPException(404,f"No predictor found for the location:{location}")
    temp = pd.DataFrame(WeatherPredictor(pool).forecast_temperature(end, location))
    humidity = pd.DataFrame(WeatherPredictor(pool).forecast_humidity(end, location))
    pressure = pd.DataFrame(WeatherPredictor(pool).forecast_pressure(end, location))
    ts = temp["ts"]
    weather_data = (
        temp.merge(humidity, on=["ts"], how="outer")
        .merge(pressure, on=["ts"], how="outer")
        .drop(columns=["ts"])
    )
    result = WeatherPredictor(pool).forecast_rain(weather_data)
    for i in range(len(result)):
        result[i]["ts"] = ts.iloc[i]
        result[i]["location"] = location
    return result


@router.get("/event/conditions")
async def get_event_conditions(location, start, end):
    try:
        start_date = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        end_date = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
    except (ValueError, TypeError):
        raise HTTPException(422, f"{start}, {end} is not of format %Y-%m-%dT%H:%M:%S")
    if start_date < datetime.now() or end_date < datetime.now():
        raise HTTPException(400, "Cannot predict past dates.")
    if start_date > end_date:
        raise HTTPException(422, "starting date greater than ending date.")
    location = location.replace(' ', '_')
    locations = WeatherPredictor(pool).get_valid_predictor_locations()
    if location not in locations:
        raise HTTPException(404,f"No predictor found for the location:{location}")
    temp = pd.DataFrame(WeatherPredictor(pool).forecast_temperature(end, location))
    humidity = pd.DataFrame(WeatherPredictor(pool).forecast_humidity(end, location))
    pressure = pd.DataFrame(WeatherPredictor(pool).forecast_pressure(end, location))
    ts = temp["ts"]
    weather_data = (
        temp.merge(humidity, on=["ts"], how="outer")
        .merge(pressure, on=["ts"], how="outer")
        .drop(columns=["ts"])
    )
    data = {}
    result = WeatherPredictor(pool).forecast_rain(weather_data)
    for i in range(len(result)):
        result[i]["ts"] = ts.iloc[i]
        result[i]["location"] = location
        result[i]["temperature"] = temp.iloc[i]["temperature"]
        result[i]["humidity"] = humidity.iloc[i]["humidity"]
    data["weather"] = result

    rain = []
    for i in range(len(result)):
        if result[i] == "rain":
            rain.append(ts.iloc[i])
    data["rain"] = rain
    weather_data = temp.merge(humidity, on=["ts"], how="outer").to_dict(
        orient="records"
    )
    summary = EventAdvisor.get_weather_conditions_summary(weather_data)
    data["max_temp"] = summary["max_temp"]
    data["max_heat"] = summary["max_heat"]
    return data


@router.post("/event/describe")
async def get_event_descriptive_advice(weather_data: EventWeatherDataList):
    weather_data = [model.model_dump() for model in weather_data.data]
    result = EventAdvisor.get_descriptive_event_advice(weather_data)
    return result


@router.get("/heatindex/")
async def get_heat_index(temp: float, humidity: float):
    heat_index = HeatIndexCalculator.calculate_heat_index(temp, humidity)
    return {"heat_index": heat_index}


@router.post("/heatindex/")
async def get_multiple_heat_index(heat_index_data: HeatIndexDataList):
    heat_index_data = [model.model_dump() for model in heat_index_data.data]
    for data in heat_index_data:
        heat_index = HeatIndexCalculator.calculate_heat_index(
            data["temperature"], data["humidity"]
        )
        data["heat_index"] = heat_index
        data.pop("temperature", None)
        data.pop("humidity", None)
    return heat_index_data


@router.get("/sensor/latest")
async def get_latest_sensor():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT ts, temperature, humidity, co
            FROM `weather_sensor`
            ORDER BY ts DESC
            LIMIT 1;
        """)
        result = cs.fetchone()
    if not result:
        raise HTTPException(404, "No sensor data found")
    return SensorData(*result)


app_api.include_router(router)
