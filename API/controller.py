import sys
from flask import abort, request, jsonify
import pymysql
from dbutils.pooled_db import PooledDB
from config import OPENAPI_STUB_DIR, DB_HOST, DB_USER, DB_PASSWD, DB_NAME

sys.path.append(OPENAPI_STUB_DIR)
from stub.swagger_server import models

pool = PooledDB(
    creator=pymysql,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWD,
    database=DB_NAME,
    maxconnections=1,
    blocking=True,
)


def get_max_temperature():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                SELECT ts, temperature
                FROM weather_predict 
                ORDER BY temperature DESC, ts 
                LIMIT 1
                """)
        result = cs.fetchone()
    if result:
        return models.Temperature(*result)
    abort(404)


def get_min_temperature():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                SELECT ts, temperature
                FROM weather_predict 
                ORDER BY temperature, ts 
                LIMIT 1
                """)
        result = cs.fetchone()
    if result:
        return models.Temperature(*result)
    abort(404)


def get_avg_temperature():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                SELECT AVG(temperature) as avg_temp
                FROM weather_predict
                """)
        result = cs.fetchone()
    if result:
        return result
    abort(404)


def get_temperature(datetime):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                    SELECT temperature, ts
                    FROM weather_predict
                    WHERE ts = (
                         SELECT ts
                         FROM weather_predict
                         ORDER BY abs(ts - %s)
                         LIMIT 1
                    );
                """, [datetime])
        result = cs.fetchone()
    if result:
        return models.Temperature(*result)
    abort(404)


def predict_temperature():
    data = request.get_json()
    datetime = data.get("datetime")
    return jsonify(datetime)


def get_max_humidity():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                SELECT ts, humidity
                FROM weather_predict 
                ORDER BY humidity DESC, ts 
                LIMIT 1
                """)
        result = cs.fetchone()
    if result:
        return models.Humidity(*result)
    abort(404)


def get_min_humidity():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                SELECT ts, humidity
                FROM weather_predict 
                ORDER BY humidity, ts 
                LIMIT 1
                """)
        result = cs.fetchone()
    if result:
        return models.Humidity(*result)
    abort(404)


def get_avg_humidity():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                SELECT AVG(humidity) as avg_humidity
                FROM weather_predict
                """)
        result = cs.fetchone()
    if result:
        return result
    abort(404)


def get_humidity(datetime):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                    SELECT humidity, ts
                    FROM weather_predict
                    WHERE ts = (
                         SELECT ts
                         FROM weather_predict
                         ORDER BY abs(ts - %s)
                         LIMIT 1
                    );
                """, [datetime])
        result = cs.fetchone()
    if result:
        return models.Humidity(*result)
    abort(404)


def predict_humidity():
    data = request.get_json()
    datetime = data.get("datetime")
    return jsonify(datetime)


def get_max_rain():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                SELECT rainfall, date
                FROM (SELECT MAX(rain_amt) as rainfall, DATE(ts) as date
                FROM weather_predict
                WHERE rain_amt > 0
                GROUP BY DATE(ts)) as rainfall
                ORDER BY rainfall DESC, date
                LIMIT 1
                """)
        result = cs.fetchone()
    if result:
        return models.Rain(*result)
    abort(404)


def get_min_rain():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                SELECT rainfall, date
                FROM (SELECT MIN(rain_amt) as rainfall, DATE(ts) as date
                FROM weather_predict
                WHERE rain_amt > 0
                GROUP BY DATE(ts)) as rainfall
                ORDER BY rainfall, date
                LIMIT 1
                """)
        result = cs.fetchone()
    if result:
        return models.Rain(*result)
    abort(404)


def get_avg_rain():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                SELECT AVG(rainfall) as avg_rainfall
                FROM (SELECT SUM(rain_amt) as rainfall
                FROM weather_predict
                GROUP BY DATE(ts)) as rainfall
                """)
        result = cs.fetchone()
    if result:
        return result
    abort(404)


def get_rain(datetime):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                    SELECT rain_amt, ts
                    FROM weather_predict
                    WHERE ts = (
                         SELECT ts
                         FROM weather_predict
                         ORDER BY abs(ts - %s)
                         LIMIT 1
                    );
                """, [datetime])
        result = cs.fetchone()
    if result:
        return models.Rain(*result)
    abort(404)


def predict_rain():
    data = request.get_json()
    datetime = data.get("datetime")
    return jsonify(datetime)


def get_heatstroke_index():
    data = request.get_json()
    humidity = data.get("humidity")
    temperature = data.get("temperature")

    heatstroke_index = temperature + humidity

    return jsonify(heatstroke_index)
