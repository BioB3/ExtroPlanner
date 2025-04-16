import streamlit as st


def keep_session_state():
    for key in st.session_state:
        if key.startswith("p_"):
            st.session_state[key] = st.session_state[key]
