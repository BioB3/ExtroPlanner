import streamlit as st

def navbar() -> None:
    with st.sidebar:
        st.title("Extroplanner")
        st.page_link('main.py', label="Home")
        st.page_link('pages/sensor.py', label="Latest sensor reading")
        st.page_link('pages/find_record.py', label="Find by datetime")
        st.page_link('pages/visualization.py', label="Visualization")
        st.page_link('pages/plan.py', label="Plan an event")
