import streamlit as st
from plotly import graph_objects
from components import navbar, render_old_data_graph
from utils import APIFetcher, keep_session_state, write_max_min

st.set_page_config(page_title="Visualization", layout="wide")
keep_session_state()
LOCATION = APIFetcher.get_location()

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

col1, col2 = st.columns([0.2, 0.8])
with col1:
    write_max_min(
        st.session_state["p_loc"],
        st.session_state["p_days"],
        st.session_state["p_atr"].lower(),
    )
with col2:
    fig = render_old_data_graph(
            y=st.session_state["p_atr"].lower(),
            location=st.session_state["p_loc"],
            days=st.session_state["p_days"],
            detail=True
            if st.session_state["p_detail"] == "Every data point"
            else False,
        )
    if type(fig) is graph_objects.Figure:
        st.plotly_chart(fig)