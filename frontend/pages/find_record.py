import streamlit as st
from datetime import datetime
from components.navbar import navbar
from utils import APIFetcher, write_closest_time, keep_session_state

st.set_page_config(page_title="Find Record", layout="wide")
keep_session_state()
LOCATION = APIFetcher.get_location()
THIRTY_MINUTES = 1800

navbar()
st.title("Find Weather data of a given time")
st.markdown(
    """
    Get the record closest to a specific time
    """
)

if "p_date" not in st.session_state:
    st.session_state["p_date"] = None
if "p_time" not in st.session_state:
    st.session_state["p_time"] = None

location_radio = st.radio("Available Locations", LOCATION, key="p_loc")
inputted_date = st.date_input("Enter date", key="p_date")
inputted_time = st.time_input("Enter time", key="p_time", step=THIRTY_MINUTES)

if inputted_date is not None and inputted_time is not None:
    write_closest_time(
        location_radio, datetime.combine(inputted_date, inputted_time)
    )
