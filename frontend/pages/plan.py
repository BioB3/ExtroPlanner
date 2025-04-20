import streamlit as st
from datetime import datetime, time, timedelta
from components import navbar, render_prediction_data
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
if "p_plan_atr" not in st.session_state:
    st.session_state["p_plan_atr"] = "Temperature"

col1, col2, col3, col4 = st.columns(4)
with col1:
    location_radio = st.radio("Available Locations", LOCATION, key="p_plan_loc")

with col2:
    start_date = st.date_input(
        "Enter the event date", key="p_start_date", min_value="today"
    )

with col3:
    start_time, end_time = st.slider(
        "Select the time range",
        value=(time(9, 00), time(12, 00)),
        step=timedelta(minutes=30),
        key="p_plan_time",
    )
with col4:
    visualized_atr = st.radio(
        "Select Attribute", options=["Temperature", "Humidity"], key="p_plan_atr"
    )

if all([start_date, start_time, end_time]):
    start_datetime = datetime.combine(start_date, start_time)
    if end_time == time(23, 59, 59, 999999):
        end_date = start_date + timedelta(days=1)
        end_datetime = datetime.combine(end_date, time(0, 0))
    else:
        end_datetime = datetime.combine(start_date, end_time)
    if start_datetime >= end_datetime:
        st.markdown("""
                    :red[Please select a valid time range]
                    """)
    else:
        st.plotly_chart(
            render_prediction_data(
                st.session_state["p_plan_atr"].lower(),
                st.session_state["p_plan_loc"],
                start_datetime,
                end_datetime,
            )
        )
