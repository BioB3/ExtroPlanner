import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from .api_fetcher import APIFetcher
from .get_unit import get_unit
from .format_datetime import format_datetime


def write_latest_data(location: str):
    try:
        data = APIFetcher.get_closest_weather(location=location)
        st.markdown(f"Last Updated: {format_datetime(data["ts"])}")
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
        st.markdown(f"*The Closest Record to {format_datetime(datetime)}*")
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
            Maximum: {max_data[attribute]} {get_unit(attribute)}\n
            on {format_datetime(max_data["ts"])}\n
            Minimum: {min_data[attribute]} {get_unit(attribute)}\n
            on {format_datetime(min_data["ts"])}
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
    temperature_humidity_data = APIFetcher.get_event_condition(
        location, now_ceil_30_mins, now_24_hrs_later
    )
    heat_index_data = APIFetcher.post_heat_index(temperature_humidity_data)
    if len(heat_index_data) == len(rain_data):
        with st.container(height=330):
            st.markdown("""
                        #### Rain and Heat index prediction for the next 24 hours
                        """)

            num_rows = 12
            num_columns = 4

            for i in range(num_rows):
                cols = st.columns(num_columns)
                for j, col in enumerate(cols):
                    if i * num_columns + j < len(rain_data):
                        k = i * num_columns + j
                        tile = col.container(height=145)
                        ts = rain_data[k]["ts"]
                        weather = rain_data[k]["weather"]
                        heat_index = heat_index_data[k]["heat_index"]
                        tile.markdown(f"""
                                    {format_datetime(ts)}\n
                                    {weather.captilize() if "rain" in weather else "No rain"}\n
                                    Heat Index: {heat_index:.2f} °C
                                    """)


def write_descriptive_advice(location: str, start: datetime, end: datetime):
    event_conditions = APIFetcher.get_event_condition(location, start, end)
    descriptive_advice = APIFetcher.post_event_describe(event_conditions)
    st.markdown(
        f"""
        Event at {location} from {format_datetime(start)} to {format_datetime(end)}\n
        Suggestion: {descriptive_advice["suggestion"]} {descriptive_advice["description"]}
        """
    )
    if descriptive_advice["items"]:
        st.markdown(f"Recommended item(s): {", ".join(descriptive_advice["items"])}")

    if descriptive_advice["rain_periods"]:
        st.markdown("Potential ran at")
        for ts_range in descriptive_advice["rain_periods"]:
            st.markdown({ts_range})

    if descriptive_advice["heat_periods"]:
        st.markdown("Potential high heat at")
        for ts_range in descriptive_advice["heat_periods"]:
            st.markdown({ts_range})
