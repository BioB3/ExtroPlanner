import streamlit as st
from components.navbar import navbar

st.set_page_config(
    page_title="Humidity"
)

navbar()
st.title("Humidity")
st.markdown(
    """
    Get more information about humidity here
    """
)