import streamlit as st
from datetime import datetime
from components import navbar, render_graph
from utils import APIFetcher, keep_session_state

st.set_page_config(page_title="Planning", layout="wide")
keep_session_state()
LOCATION = APIFetcher.get_location()
THIRTY_MINUTES = 1800

navbar()
st.title("Planning an Event")

if "p_plan_loc" not in st.session_state:
    st.session_state["p_plan_loc"] = LOCATION[0]
if "p_start_date" not in st.session_state:
    st.session_state["p_start_date"] = None
if "p_start_time" not in st.session_state:
    st.session_state["p_start_time"] = None
if "p_end_date" not in st.session_state:
    st.session_state["p_end_date"] = None
if "p_end_time" not in st.session_state:
    st.session_state["p_end_time"] = None

col1, col2, col3 = st.columns(3)
with col1:
    location_radio = st.radio("Available Locations", LOCATION, key="p_plan_loc")

with col2:
    start_date = st.date_input("Enter the starting date", key="p_start_date")
    start_time = st.time_input(
        "Enter the starting time", key="p_start_time", step=THIRTY_MINUTES
    )

with col3:
    end_date = st.date_input("Enter the end date", key="p_end_date")
    end_time = st.time_input(
        "Enter the end time", key="p_end_time", step=THIRTY_MINUTES
    )

if all([start_date, start_time, end_date, end_time]):
    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = datetime.combine(end_date, end_time)
    if(start_datetime >= end_datetime):
        st.markdown("""
                    :red[Please select a valid time range]
                    """)
    else:
        st.markdown(f"""
                    Planned Event\n
                    Datetime: {datetime.combine(start_date, start_time)} -
                    {datetime.combine(end_date, end_time)}\n
                    Location: {location_radio}
                    """)
