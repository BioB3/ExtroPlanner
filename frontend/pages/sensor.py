import streamlit as st
from components import navbar
import pandas as pd
from utils import keep_session_state, APIFetcher, format_datetime

st.set_page_config(page_title="Sensor Reading", layout="wide")
keep_session_state()

navbar()
st.title("Latest Sensor Reading")


def encode_co(co_value: float):
    if co_value < 14:
        return "normal"
    elif co_value < 25:
        return "poor"
    elif co_value < 35:
        return "unhealthy"
    else:
        return "abnormal"


def get_warnings_tips(co_value: float):
    if co_value < 14:
        return "Normal CO levels."
    elif co_value < 25:
        return "Moderate contamination risk.\nSymptoms may devolop at this level.\n\
Leave the area if you feel unwell.\nPeople with heart/lung issues should call their doctor."
    elif co_value < 35:
        return "Serious risk.\nSymptoms likely, especially for vulnerable.\n\
Evacuate as fast as you could even if symptoms are mild or absent."
    else:
        return "Extreme risk.\nLife-threatening for all.\n\
Evacuate immediately and call emergency services."


try:
    data = APIFetcher.get_latest_sensor()
    st.markdown(f"Last Updated: {format_datetime(data['ts'])}")
    df = pd.DataFrame.from_dict([data]).drop(columns=["ts"])
    df["co"] = df["co"].apply(encode_co)
    st.table(df)
    st.markdown(get_warnings_tips(data["co"]))

except ValueError as e:
    error_message = str(e)
    if "500" in error_message:
        st.markdown(":red[Could not connect to the database]")
    elif "404" in error_message:
        st.markdown(":red[No data is found]")
