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

# #####################################################################
# # 제목 : 서브 페이지
# # 수정 날짜 : 2024-07-10
# # 작성자 : 장재혁
# # 수정자 : 장지헌
# # 수정 내용 : 교과서 영역 레이아웃
# #####################################################################

# 파일 불러오기
import stt, voca, helper, ai_chatbot

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
    # st.set_page_config(layout="wide")

    with st.sidebar:
        choose = option_menu("VONDI", ['AI 속기사', '수어 번역', '수어 사전', '노트 필기'],
                            icons=['bi bi-card-text', 'bi bi-journal', 'bi bi-file-play'],
                            menu_icon="app-indicator", default_index=0,
                            styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        })
        # 사이드바 맨 아래에 '나가기' 버튼 추가
        st.sidebar.markdown("<br>" * 10, unsafe_allow_html=True)  # 간격 추가
        if st.sidebar.button("나가기"):
            st.session_state.sub_page = False
            st.experimental_rerun()

    # Recognizer 객체 생성
    recognizer = sr.Recognizer()

    # if choose == "STT":
    #     col1, col2 = st.columns([2, 1])
        
    #     with col1:
    #         st.image("image\국어내용.png", caption="국어")
    #         if st.button("자막"):
    #             result = speech_to_text(recognizer)
                
    #     with col2:
    #         stt.main()

    if choose == "AI 속기사":
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image("image\국어내용.png", caption="국어")
            if st.button("자막"):
                result = speech_to_text(recognizer)
                
        with col2:
            ai_chatbot.main()
            
    elif choose == "수어 번역":
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image("image\국어내용.png", caption="국어")
            helper.main()
                
        with col2:
            ai_chatbot.main()
            
    elif choose == "수어 사전":
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image("image\국어내용.png", caption="국어")
            voca.main()
            
        with col2:
            ai_chatbot.main()
            
    elif choose == "노트 필기":
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image("image\국어내용.png", caption="국어")
            # 노트 필기 함수 추가
            
        with col2:
            ai_chatbot.main()