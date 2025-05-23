import requests
import streamlit as st
import pandas as pd
from datetime import datetime


class APIFetcher:
    __BASE_URL = "http://127.0.0.1:8000/explan"

    @classmethod
    @st.cache_data
    def get_location(cls):
        response = requests.get(f"{cls.__BASE_URL}/locations")
        if response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.text}")
        return [location for location in response.json()]

    @classmethod
    def get_closest_weather(cls, location: str, datetime: datetime | None = None):
        url = f"{cls.__BASE_URL}/weather?location={location}"
        if datetime is not None:
            url += f"&datetime={datetime.isoformat()}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.text}")
        return response.json()

    @classmethod
    @st.cache_data
    def get_last_days_weather(cls, location: str, days: int | None = None):
        url = f"{cls.__BASE_URL}/weather/last?location={location}"
        if days is not None:
            url += f"&days={days}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.text}")
        return response.json()

    @classmethod
    @st.cache_data
    def get_aggregate_weather(cls, location: str, days: int | None = None):
        url = f"{cls.__BASE_URL}/weather/aggregate?location={location}"
        if days is not None:
            url += f"&days={days}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.text}")
        return response.json()

    @classmethod
    @st.cache_data
    def get_max_min(cls, location: str, attribute: str, days: int | None = None):
        max_url = f"{cls.__BASE_URL}/{attribute}/max?location={location}"
        min_url = f"{cls.__BASE_URL}/{attribute}/min?location={location}"
        if days is not None:
            days_param = f"&days={days}"
            max_url += days_param
            min_url += days_param
        max_response = requests.get(max_url)
        min_response = requests.get(min_url)
        if max_response.status_code != 200:
            raise ValueError(f"{max_response.status_code}: {max_response.text}")
        if min_response.status_code != 200:
            raise ValueError(f"{min_response.status_code}: {min_response.text}")
        return (max_response.json(), min_response.json())

    @classmethod
    @st.cache_data
    def get_temperature_prediction(cls, location: str, start: datetime, end: datetime):
        url = f"{cls.__BASE_URL}/predict/temperature?location={location}&ts={end.isoformat()}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.text}")
        data = response.json()
        df = pd.DataFrame.from_dict(data)
        return df[df["ts"] >= start.isoformat()]

    @classmethod
    @st.cache_data
    def get_humidity_prediction(cls, location: str, start: datetime, end: datetime):
        url = f"{cls.__BASE_URL}/predict/humidity?location={location}&ts={end.isoformat()}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.text}")
        data = response.json()
        df = pd.DataFrame.from_dict(data)
        return df[df["ts"] >= start.isoformat()]

    @classmethod
    @st.cache_data
    def get_rain_prediction(cls, location: str, start: datetime, end: datetime):
        url = f"{cls.__BASE_URL}/predict/rain?location={location}&start={start.isoformat()}\
&end={end.isoformat()}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.text}")
        return [entry for entry in response.json() if entry["ts"] >= start.isoformat()]

    @classmethod
    @st.cache_data
    def get_event_condition(cls, location: str, start: datetime, end: datetime):
        url = f"{cls.__BASE_URL}/event/conditions?location={location}\
&start={start.isoformat()}&end={end.isoformat()}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.text}")
        return [
            entry
            for entry in response.json()["weather"]
            if entry["ts"] >= start.isoformat()
        ]

    @classmethod
    @st.cache_data
    def post_event_describe(cls, weather_data: list):
        url = f"{cls.__BASE_URL}/event/describe"
        body = {"data": weather_data}
        response = requests.post(url, json=body)
        if response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.text}")
        return response.json()

    @classmethod
    @st.cache_data
    def get_heat_index(cls, temperature: float, humidity: float):
        url = f"{cls.__BASE_URL}/heatindex/?temp={temperature}&humidity={humidity}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.text}")
        return response.json()

    @classmethod
    @st.cache_data
    def post_heat_index(cls, temp_humidity_data: list):
        url = f"{cls.__BASE_URL}/heatindex/"
        body = {"data": temp_humidity_data}
        response = requests.post(url, json=body)
        if response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.text}")
        return response.json()

    @classmethod
    def get_latest_sensor(cls):
        url = f"{cls.__BASE_URL}/sensor/latest"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.text}")
        return response.json()
