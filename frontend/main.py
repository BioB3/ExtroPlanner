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
write_latest_data(st.session_state["p_loc"])

with st.container(height=170):
    st.markdown("""
                #### Rain and Heat index prediction for the next 24 hours
                """)

    num_rows = 12
    num_columns = 4

    for _ in range(num_rows):
        cols = st.columns(num_columns)
        for col in cols:
            tile = col.container(height=50)