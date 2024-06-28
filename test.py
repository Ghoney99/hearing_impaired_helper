import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from PIL import Image
import numpy as np
import pandas as pd
import plotly.express as px
import io
from tkinter.tix import COLUMN
from pyparsing import empty
from openai import OpenAI

# 터미널 창에 입력해서 실행
# streamlit run test.py

st.set_page_config(layout="wide")

#####################################################################
# 수정 날짜 : 2024-06-28
# 작성자 : 장재혁
# 수정자 : 장지헌
# 수정 내용 : 수어 단어장 추가
#####################################################################
with st.sidebar:
    choose = option_menu("AI 디지털 교과서", ["STT", "수어 도우미", "AI Tutor", '수어 단어장'],
                         icons=['house', 'camera fill', 'kanban'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )
#####################################################################



#####################################################################
# 수정 날짜 : 2024-06-28
# 작성자 : 장재혁
# 수정자 : 장지헌
# 수정 내용 : 
#####################################################################
if choose == "AI Tutor":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.image("20240627_214541.png", caption="국어", use_column_width=True)

    with col2:
        st.title("AI 튜터")

        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo"

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("What is up?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
#####################################################################


#####################################################################
# 수정 날짜 : 2024-06-28
# 작성자 : 장재혁
# 수정자 : 장재혁
# 수정 내용 : 
#####################################################################
elif choose == "STT":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.image("20240627_214541.png", caption="국어", use_column_width=True)

    with col2:
        st.title("Speech-to-Text (STT) App")
        st.write("STT 관련 콘텐츠")
#####################################################################


#####################################################################
# 수정 날짜 : 2024-06-28
# 작성자 : 장지헌
# 수정자 : 장지헌
# 수정 내용 : 
#####################################################################
elif choose == "수어 도우미":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.image("20240627_214541.png", caption="국어", use_column_width=True)

    with col2:
        st.title("수어 도우미 (Sign Language Helper) App")
        st.write("수어 도우미 관련 콘텐츠")
#####################################################################


#####################################################################
# 수정 날짜 : 2024-06-28
# 작성자 : 장지헌
# 수정자 : 장지헌
# 수정 내용 : 
#####################################################################
elif choose == "수어 단어장":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.image("20240627_214541.png", caption="국어", use_column_width=True)

    with col2:
        st.title("수어 단어장 (Sign Language Helper) App")
        st.write("수어 단어장")
#####################################################################