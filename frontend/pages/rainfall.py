import streamlit as st
from components.navbar import navbar

st.set_page_config(
    page_title="Rainfall"
)

navbar()
st.title("Rainfall")
st.markdown(
    """
    Get more information about rainfall here
    """
)