import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from .api_fetcher import APIFetcher


def write_latest_data(location: str):
    try:
        data = APIFetcher.get_closest_weather(location=location)
        st.markdown(
            f"Last Updated: {datetime.strptime(data["ts"], "%Y-%m-%dT%H:%M:%S")}"
        )
        df = pd.DataFrame.from_dict([data]).drop(columns=["ts"])
        st.table(df)
    except ValueError as e:
        error_message = str(e)
        if "500" in error_message:
            st.markdown(":red[Could not connect to the database]")
        elif "404" in error_message:
            st.markdown(":red[No data is found]")


def write_closest_time(location: str, datetime: datetime):
    try:
        data = APIFetcher.get_closest_weather(location, datetime)
        st.markdown(f"*The Closest Record to {datetime}*")
        df = pd.DataFrame.from_dict([data]).drop(columns=["ts"])
        st.table(df)
    except ValueError as e:
        error_message = str(e)
        if "500" in error_message:
            st.markdown(":red[Could not connect to the database]")
        elif "404" in error_message:
            st.markdown(":red[No data is found]")


def write_max_min(location: str, days: int, attribute: str):
    try:
        max_data, min_data = APIFetcher.get_max_min(location, attribute, days)
        st.markdown("***")
        st.markdown(
            f"""
            {attribute.capitalize()} of the past {days} day(s)\n
            Maximum: {max_data[attribute]} \n
            on {datetime.strptime(max_data["ts"], "%Y-%m-%dT%H:%M:%S")}\n
            Minimum: {min_data[attribute]} \n
            on {datetime.strptime(min_data["ts"], "%Y-%m-%dT%H:%M:%S")}
            """
        )
    except ValueError as e:
        error_message = str(e)
        if "500" in error_message:
            st.markdown(":red[Could not connect to the database]")
        elif "404" in error_message:
            st.markdown(f":red[No data found within today and {days} day(s) ago]")


def write_24hrs_rain_heat_prediction(location):
    now = datetime.now()
    now_ceil_30_mins = now + (datetime.min - now) % timedelta(minutes=30)
    now_24_hrs_later = now_ceil_30_mins + timedelta(days=1)
    rain_data = APIFetcher.get_rain_prediction(
        location, now_ceil_30_mins, now_24_hrs_later
    )
    filtered_data = [entry for entry in rain_data if entry["ts"] >= now.isoformat()]
    with st.container(height=330):
        st.markdown("""
                    #### Rain and Heat index prediction for the next 24 hours
                    """)

        num_rows = 12
        num_columns = 4

        for i in range(num_rows):
            cols = st.columns(num_columns)
            for j, col in enumerate(cols):
                if i * num_columns + j <len(filtered_data):
                    tile = col.container(height=120)
                    ts = filtered_data[i * num_columns + j]["ts"]
                    weather = filtered_data[i * num_columns + j]["weather"]
                    tile.markdown(f"""
                                {datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")}\n
                                {weather.captilize() if "rain" in weather else "No rain"}
                                """)
                    
