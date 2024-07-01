import streamlit as st

def get_session_state(**kwargs):
    session_state = st.session_state

    for key, value in kwargs.items():
        if key not in session_state:
            session_state[key] = value

    return session_state