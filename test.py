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
plt.rcParams['font.family'] ='Malgun Gothic'

st.set_page_config(layout="wide")

with st.sidebar:
    choose = option_menu("AI 디지털 교과서", ["STT", "수어 도우미", "AI Tutor",'성적 확인'],
                         icons=['house', 'camera fill', 'kanban'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )

if choose == "AI Tutor":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.image("20240627_214541.png", caption="국어", use_column_width=True)
        
        
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
        

elif choose == "STT":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.image("20240627_214541.png", caption="국어", use_column_width=True)

    with col2:
        st.title("Speech-to-Text (STT) App")
        st.write("STT 관련 콘텐츠")
    
elif choose == "수어 도우미":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.image("20240627_214541.png", caption="국어", use_column_width=True)

    with col2:
        st.title("수어 도우미 (Sign Language Helper) App")
        st.write("수어 도우미 관련 콘텐츠")
        
elif choose == "성적 확인":
    # 데이터셋 로드
    df = pd.read_csv('student_scores_korean_subjects.csv')

    # Ensure relevant columns are numeric
    for col in ['국어_중간고사', '국어_기말고사', '수학_중간고사', '수학_기말고사', '영어_중간고사', '영어_기말고사', '과학_중간고사', '과학_기말고사']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 학생 이름과 ID를 매핑
    student_name_to_id = {row['이름']: row['학생ID'] for _, row in df.iterrows()}

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

    # 사용자에게 이름을 입력받음
    student_name = st.text_input('학생 이름을 입력하세요:')
    if student_name:
        if student_name in student_name_to_id:
            student_id = student_name_to_id[student_name]
            compare_student_with_average(df, student_id)
        else:
            st.write("해당 이름의 학생을 찾을 수 없습니다.")