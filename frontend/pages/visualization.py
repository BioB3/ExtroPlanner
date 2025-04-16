import streamlit as st
from datetime import datetime
from components import navbar, render_graph
from utils import APIFetcher, keep_session_state

st.set_page_config(page_title="Temperature", layout="wide")
keep_session_state()
LOCATION = APIFetcher.get_location()
THIRTY_MINUTES = 1800

navbar()
st.title("Visualization")

if "p_detail" not in st.session_state:
    st.session_state["p_detail"] = "Average of the day"
if "p_days" not in st.session_state:
    st.session_state["p_days"] = 7
if "p_atr" not in st.session_state:
    st.session_state["p_atr"] = "Temperature"

col1, col2, col3, col4 = st.columns([0.25, 0.25, 0.25, 0.25])
with col1:
    location_radio = st.radio("Available Locations", LOCATION, key="p_loc")

with col2:
    detail_radio = st.radio(
        "Detail Level", ["Average of the day", "Every data point"], key="p_detail"
    )

with col3:
    visualized_atr = st.radio(
        "Select Attribute", options=["Temperature", "Humidity", "Rainfall"], key="p_atr"
    )

with col4:
    num_days = st.select_slider(
        "Select number of days in the past", options=[1, 7, 14, 30], key="p_days"
    )

try:
    st.plotly_chart(
        render_graph(
            y=st.session_state["p_atr"].lower(),
            location=st.session_state["p_loc"],
            days=st.session_state["p_days"],
            detail=True if st.session_state["p_detail"] == "Every data point" else False,
        )
    )
except ValueError:
    st.markdown(f"No data found within today and {st.session_state["p_days"]} day(s) ago")
