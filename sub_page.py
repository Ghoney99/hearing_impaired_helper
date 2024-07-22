import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from PIL import Image
import numpy as np
import pandas as pd
import plotly.express as px
import io
# from tkinter.tix import COLUMN
from pyparsing import empty
import matplotlib.pyplot as plt
from openai import OpenAI
import speech_recognition as sr

# #####################################################################
# # 제목 : 서브 페이지
# # 수정 날짜 : 2024-07-16
# # 작성자 : 장재혁
# # 수정자 : 장재혁
# # 수정 내용 : 배경 넣고 요소들 삭제
# #####################################################################

# 파일 불러오기
import stt, voca, helper, ai_chatbot, background

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
    background.add_bg_from_url4()

    with st.sidebar:
        st.image('image\logo.png')
        choose = option_menu(menu_title=None, options=['AI 속기사', '수어 번역', '수어 사전', 'AI비서'],
                            icons=['bi bi-card-text', 'bi bi-journal', 'bi bi-file-play'],
                            menu_icon="app-indicator", default_index=0,
                           styles={
                    "container": {"padding": "5!important", "background-color": "#e6f2ff"},  # 연한 푸른색 배경
                    "icon": {"color": "#0066cc", "font-size": "25px"},  # 아이콘 색상을 진한 푸른색으로
                    "nav-link": {
                        "font-size": "16px", 
                        "text-align": "left", 
                        "margin": "0px", 
                        "--hover-color": "#99ccff",  # 호버 시 연한 푸른색
                        "color": "#000033",  # 텍스트 색상을 진한 남색으로
                    },
                    "nav-link-selected": {"background-color": "#3399ff"},  # 선택된 항목 배경색을 중간 톤의 푸른색으로
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
        st.title('')
        st.title('')
        st.title('')
        st.title('')
        st.title('')


        if st.button("자막"):
            result = speech_to_text(recognizer)
            
    elif choose == "수어 번역":
        helper.main()
            
    elif choose == "수어 사전":
        # 배경
        background.add_bg_from_url6()
        
        voca.main()
            
    elif choose == "AI비서":
        # 배경
        background.add_bg_from_url5()
        
        ai_chatbot.main()