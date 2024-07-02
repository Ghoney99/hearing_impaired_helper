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
import speech_recognition as sr

# 파일 불러오기
import stt, voca, helper

# 글꼴 설정
plt.rcParams['font.family'] ='Malgun Gothic'

# STT 함수
def speech_to_text(recognizer):
    with sr.Microphone() as source:
        # st.write("[자막]")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language='ko-KR')
        st.subheader(f"{text}") # 결과값 출력
        return text
    except sr.UnknownValueError:
        st.write("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        st.write(f"음성 인식 서비스에 접근할 수 없습니다: {e}")


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
    
    # Recognizer 객체 생성
    recognizer = sr.Recognizer()
    
    if choose == "STT":
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image("image\국어내용.png", caption="국어")
            if st.button("자막"):
                result = speech_to_text(recognizer)
                            
        with col2:
            stt.main()
            
    elif choose == "수어 단어장":
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image("image\국어내용.png", caption="국어")
            if st.button("자막"):
                result = speech_to_text(recognizer)
            
        with col2:
            voca.main()
  
    elif choose == "수어 도우미":
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image("image\국어내용.png", caption="국어")
            if st.button("자막"):
                result = speech_to_text(recognizer)       
                     
        with col2:
            helper.main()
