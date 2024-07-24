import streamlit as st

def get_session_state(**kwargs):
    # Streamlit의 session_state를 초기화하고 반환하는 함수
    # 매개변수: **kwargs: 키워드 인자로 전달되는 초기 상태값들
    # 반환값: st.session_state: 초기화된 Streamlit의 session_state 객체
    session_state = st.session_state

    for key, value in kwargs.items():
        if key not in session_state:
            session_state[key] = value

    return session_state