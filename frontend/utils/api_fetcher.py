import requests
import streamlit as st
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
            max_url +=  days_param
            min_url += days_param
        max_response = requests.get(max_url)
        min_response = requests.get(min_url)
        if max_response.status_code != 200:
            raise ValueError(f"{max_response.status_code}: {max_response.text}")
        if min_response.status_code != 200:
            raise ValueError(f"{min_response.status_code}: {min_response.text}")
        return (max_response.json(), min_response.json())
