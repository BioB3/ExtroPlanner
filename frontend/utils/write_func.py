import streamlit as st
import pandas as pd
from datetime import datetime
from .api_fetcher import APIFetcher


def write_latest_data(location: str):
    data = APIFetcher.get_closest_weather(location=location)
    st.markdown(f"Last Updated: {datetime.strptime(data["ts"], "%Y-%m-%dT%H:%M:%S")}")
    df = pd.DataFrame.from_dict([data]).drop(columns=["ts"])
    st.table(df)


def write_closest_time(location: str, datetime: datetime):
    data = APIFetcher.get_closest_weather(location, datetime)
    st.markdown(f"*The Closest Record to {datetime}*")
    df = pd.DataFrame.from_dict([data]).drop(columns=["ts"])
    st.table(df)


def write_historical(location: str, days: int, key: str):
    data = APIFetcher.get_last_days_weather(location, days)
    df = pd.DataFrame.from_dict
