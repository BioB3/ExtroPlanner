import streamlit as st
from components import navbar
import pandas as pd
from utils import keep_session_state, APIFetcher, format_datetime

st.set_page_config(page_title="Sensor Reading", layout="wide")
keep_session_state()

navbar()
st.title("Latest Sensor Reading")

try:
    data = APIFetcher.get_latest_sensor()
    st.markdown(f"Last Updated: {format_datetime(data["ts"])}")
    df = pd.DataFrame.from_dict([data]).drop(columns=["ts"])
    st.table(df)
except ValueError as e:
    error_message = str(e)
    if "500" in error_message:
        st.markdown(":red[Could not connect to the database]")
    elif "404" in error_message:
        st.markdown(":red[No data is found]")
