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
                """)
    abort(404)


def get_min_temperature():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                """)
    abort(404)


def get_avg_temperature():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                """)
    abort(404)


def get_temperature(datetime):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                """)
    abort(404)


def predict_temperature():
    data = request.get_json()
    datetime = data.get("datetime")
    return jsonify(datetime)


def get_max_humidity():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                """)
    abort(404)


def get_min_humidity():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                """)
    abort(404)


def get_avg_humidity():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                """)
    abort(404)


def get_humidity(datetime):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                """)
    abort(404)


def predict_humidity():
    data = request.get_json()
    datetime = data.get("datetime")
    return jsonify(datetime)


def get_max_rain():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                """)
    abort(404)


def get_min_rain():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                """)
    abort(404)


def get_avg_rain():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                """)
    abort(404)


def get_rain(datetime):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                """)
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
