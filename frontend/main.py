import streamlit as st
from components import navbar
from utils import APIFetcher, write_latest_data, keep_session_state

st.set_page_config(page_title="Home", layout="wide")
keep_session_state()
LOCATION = APIFetcher.get_location()

navbar()
st.title("ExtroPlanner")
st.markdown(
    """
    View the latest :red[temperature], :green[humidity] and :blue[rainfall] reading here.
    """
)

if "p_loc" not in st.session_state:
    st.session_state["p_loc"] = LOCATION[0]

location_radio = st.radio("Available Locations", LOCATION, key="p_loc")
st.markdown("Latest Reading")
write_latest_data(st.session_state["p_loc"])
