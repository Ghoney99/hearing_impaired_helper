import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import speech_recognition as sr
from openai import OpenAI
import voca, helper, ai_chatbot, background

#####################################################################
# 제목 : 서브 페이지
# 수정 날짜 : 2024-07-24
# 작성자 : 장재혁
# 수정자 : 장지헌
# 수정 내용 : 라이브러리 정리
#####################################################################

# 글꼴 설정
plt.rcParams['font.family'] ='Malgun Gothic'


# STT 함수 / 음성을 텍스트로 변환하는 함수
# 매개변수: recognizer (speech_recognition.Recognizer): 음성 인식기 객체
# 반환값: str 또는 None: 인식된 텍스트 또는 인식 실패 시 None
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
                            icons=['bi bi-card-text', 'bi bi-journal', 'bi bi-file-play', 'bi bi-robot'],
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