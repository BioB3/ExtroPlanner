import streamlit as st

def navbar() -> None:
    with st.sidebar:
        st.page_link('main.py', label="Home")
        st.page_link('pages/temperature.py', label="Temperature")
        st.page_link('pages/humidity.py', label="Humidity")
        st.page_link('pages/rainfall.py', label="Rainfall")