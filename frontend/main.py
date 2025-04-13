import streamlit as st
from components.navbar import navbar

st.set_page_config(
    page_title="Home"
)

navbar()
st.title("ExtroPlanner")
st.markdown(
    """
    View the latest :red[temperature], :green[humidity] and :blue[rainfall] reading here.
    """
)
