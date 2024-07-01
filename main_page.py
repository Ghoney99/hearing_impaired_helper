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
import sub_page

from utils import get_session_state

# 세션 상태 가져오기
session_state = get_session_state(sub_page=False)
# 글꼴 설정
plt.rcParams['font.family'] ='Malgun Gothic'

def compare_student_with_average(df, student_id):
        student_data = df[df['학생ID'] == student_id]

        df['전체_평균_국어'] = df[['국어_중간고사', '국어_기말고사']].mean(axis=1)
        df['전체_평균_수학'] = df[['수학_중간고사', '수학_기말고사']].mean(axis=1)
        df['전체_평균_영어'] = df[['영어_중간고사', '영어_기말고사']].mean(axis=1)
        df['전체_평균_과학'] = df[['과학_중간고사', '과학_기말고사']].mean(axis=1)

        semester_avg = df.groupby('학기').mean(numeric_only=True).reset_index()

        student_data['학생_평균_국어'] = student_data[['국어_중간고사', '국어_기말고사']].mean(axis=1)
        student_data['학생_평균_수학'] = student_data[['수학_중간고사', '수학_기말고사']].mean(axis=1)
        student_data['학생_평균_영어'] = student_data[['영어_중간고사', '영어_기말고사']].mean(axis=1)
        student_data['학생_평균_과학'] = student_data[['과학_중간고사', '과학_기말고사']].mean(axis=1)

        student_avg = student_data.groupby('학기').mean(numeric_only=True).reset_index()

        fig, axs = plt.subplots(2, 2, figsize=(14, 10))
        subjects = ['국어', '수학', '영어', '과학']
        for i, subject in enumerate(subjects):
            ax = axs[i // 2, i % 2]
            ax.plot(semester_avg['학기'], semester_avg[f'전체_평균_{subject}'], label='전체 평균', marker='o')
            ax.plot(student_avg['학기'], student_avg[f'학생_평균_{subject}'], label='학생 평균', marker='o')
            ax.set_title(f'{subject} 성적 비교')
            ax.set_xlabel('학기')
            ax.set_ylabel('평균 성적')
            ax.legend()

        plt.tight_layout()
        st.pyplot(fig)


def main():
    if session_state.sub_page:
        sub_page.main()
    else:
        
    
        st.set_page_config(layout="wide")

        with st.sidebar:
            choose = option_menu("VONDI", ['마이페이지', "교과서"],
                                icons=['house', 'bi bi-journals'],
                                menu_icon="app-indicator", default_index=0,
                                styles={
                "container": {"padding": "5!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#02ab21"},
        }
        )
        if choose == "마이페이지":
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.title("최수아")
                st.write("성적 확인")
                df = pd.read_csv('student_scores_korean_subjects.csv')
                for col in ['국어_중간고사', '국어_기말고사', '수학_중간고사', '수학_기말고사', '영어_중간고사', '영어_기말고사', '과학_중간고사', '과학_기말고사']:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

                # 학생 이름과 ID를 매핑
                student_name_to_id = {row['이름']: row['학생ID'] for _, row in df.iterrows()}
                student_id = student_name_to_id['최수아']
                compare_student_with_average(df, student_id)

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
        
        
        if choose == "교과서":   

            # 세 개의 컬럼 만들기
            col1, col2, col3 = st.columns(3)

            # 첫 번째 컬럼에 이미지와 텍스트, 버튼 추가
            with col1:
                st.image("image\국어표지1.png", caption="국어")
                st.text("국어")
                if st.button("국어"):
                    session_state.sub_page = True
                    st.experimental_rerun()  # 페이지 리로드

            # 두 번째 컬럼에 이미지와 텍스트, 버튼 추가
            with col2:
                st.image("image\수학표지1.png", caption="수학")
                st.text("수학")
                if st.button("수학"):
                    st.write("수학 버튼을 눌렀습니다.")

            # 세 번째 컬럼에 이미지와 텍스트, 버튼 추가
            with col3:
                st.image("image\영어표지1.jpg", caption="영어")
                st.text("영어")
                if st.button("영어"):
                    st.write("영어 버튼을 눌렀습니다.")