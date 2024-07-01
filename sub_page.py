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
import matplotlib.pyplot as plt
from openai import OpenAI

# 글꼴 설정
plt.rcParams['font.family'] ='Malgun Gothic'

def main():
    st.set_page_config(layout="wide")

    with st.sidebar:
        choose = option_menu("VONDI", ["STT", '수어 단어장', "수어 도우미"],
                            icons=['bi bi-card-text', 'bi bi-journal', 'bi bi-file-play'],
                            menu_icon="app-indicator", default_index=0,
                            styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
    }
    )
    if choose == "STT":
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image("image\국어내용.png", caption="국어")
            
            
        with col2:
            st.title("AI 튜터")

            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            if "openai_model" not in st.session_state:
                st.session_state["openai_model"] = "ft:gpt-3.5-turbo-0125:personal::9evZE1BR"

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