import streamlit as st
from datetime import datetime
from components.navbar import navbar

THIRTY_MINUTES = 1800

st.set_page_config(
    page_title="Temperature"
)

navbar()
st.title("Temperature")
st.markdown(
    """
    Get more information about temperature here
    """
)
inputted_date = st.date_input("Enter date", value=None)
st.write("Inputted date is", inputted_date)
inputted_time = st.time_input("Enter time", value=None, step=THIRTY_MINUTES)
st.write("Inputted time is", inputted_time)

if inputted_date is not None and inputted_time is not None:
    st.write("Combined datetime", datetime.combine(inputted_date, inputted_time))
