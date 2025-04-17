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


def write_max_min(location: str, days: int, attribute: str):
    max_data, min_data = APIFetcher.get_max_min(location, attribute, days)
    st.markdown(
        f"Maximum {attribute} of the past {days} day(s) is {max_data[attribute]} on\
    {datetime.strptime(max_data["ts"], "%Y-%m-%dT%H:%M:%S")}"
    )
    st.markdown(
        f"Minimum {attribute} of the past {days} day(s) is {min_data[attribute]} on\
    {datetime.strptime(min_data["ts"], "%Y-%m-%dT%H:%M:%S")}"
    )
