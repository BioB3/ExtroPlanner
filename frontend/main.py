import streamlit as st
from components import navbar
from utils import (
    APIFetcher,
    write_latest_data,
    keep_session_state,
    write_24hrs_rain_heat_prediction,
)

st.set_page_config(page_title="Home", layout="wide")
keep_session_state()
LOCATION = APIFetcher.get_location()

navbar()
st.title("ExtroPlanner")
st.markdown(
    """
    View the latest :red[temperature], :green[humidity] and :blue[rainfall]
    or view the rain and heat index predictions.
    """
)

tab1, tab2 = st.tabs(["Latest Reading", "Predictions"])

with tab1:
    st.markdown("#### Latest Reading")
    if "p_loc" not in st.session_state:
        st.session_state["p_loc"] = LOCATION[0]

    location_radio = st.radio("Available Locations", LOCATION, key="p_loc")
    write_latest_data(st.session_state["p_loc"])

with tab2:
    write_24hrs_rain_heat_prediction(st.session_state["p_loc"])
