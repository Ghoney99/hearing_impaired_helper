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

# 파일불러오기
import sub_page, ai_chatbot

# 페이지 전환
from utils import get_session_state

# 글꼴 설정
plt.rcParams['font.family'] ='Malgun Gothic'

def score_plot(file_path, s_name):
    st.title('학년별 성적 조회')

    df = pd.read_csv(file_path)
    student_name = s_name

    # 학년 선택
    grade = st.slider('학년 선택:', min_value=1, max_value=6, value=(1, 6))

    # 선택된 데이터 필터링
    filtered_data = df[(df['Name'] == student_name) & (df['Grade'].between(grade[0], grade[1]))]

    # 과목 체크박스 생성 (국어 기본 선택)
    default_subjects = ['국어']
    subjects = st.multiselect('과목 선택:', filtered_data['Subject'].unique(), default=default_subjects)

    # 전체 학생 데이터 로드
    all_students_data = df[df['Grade'].between(grade[0], grade[1])]

    # 그래프 그리기
    if not filtered_data.empty:
        plt.figure(figsize=(10, 6))

        # 각 과목의 선택된 학생 데이터 그리기
        for subject in subjects:
            subject_data = filtered_data[filtered_data['Subject'] == subject]
            plt.plot(subject_data['Total_Semester'], subject_data['Score'], marker='o', label=f'{student_name} - {subject}')

        # 전체 학생의 각 과목 평균 성적 계산 및 그리기
        for subject in subjects:
            subject_data_all = all_students_data[all_students_data['Subject'] == subject]
            avg_scores = subject_data_all.groupby('Total_Semester')['Score'].mean()
            plt.plot(avg_scores.index, avg_scores.values, linestyle='--', label=f'{subject} 전체 평균')

        plt.xlabel('학기')
        plt.ylabel('성적')
        plt.title(f'{student_name}학생의 {grade[0]} ~ {grade[1]} 학년 성적')
        plt.legend()
        st.pyplot(plt)
        

def radar_plot(file_path, student_name):
    # 데이터 읽기
    df = pd.read_csv(file_path)

    # 학생 데이터 필터링
    student_data = df[df['Name'] == student_name]

    # 학년 및 학기 선택 옵션 생성
    unique_grades = student_data['Grade'].unique()
    unique_semesters = student_data['Semester'].unique()

    # 학년 및 학기 선택
    selected_grade = st.selectbox(f"{student_name} 학생의 학년", unique_grades)
    selected_semester = st.selectbox(f"{selected_grade}학년 학기", unique_semesters)

    # 선택한 학년 및 학기의 데이터 필터링
    filtered_data = student_data[(student_data['Grade'] == selected_grade) & (student_data['Semester'] == selected_semester)]

    # 방사형 그래프 생성
    if not filtered_data.empty:
        subjects = filtered_data['Subject'].unique()
        scores = [filtered_data[filtered_data['Subject'] == subject]['Score'].values[0] for subject in subjects]

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_rlim(0, 100)
        ax.set_thetagrids(np.arange(0, 360, 360 / len(subjects)), subjects)
        ax.plot(np.radians(np.arange(0, 360, 360 / len(subjects))), scores, 'o', color='blue', alpha=0.7)
        ax.fill(np.radians(np.arange(0, 360, 360 / len(subjects))), scores, alpha=0.2)
        ax.set_title(f"{student_name} 학생의 {selected_grade}학년 {selected_semester}학기 성적")

        st.pyplot(fig)
    else:
        st.write("해당 학년 및 학기의 데이터가 없습니다.")


def main(name):
    # 세션 상태 가져오기
    session_state = get_session_state(sub_page=False)
    if not session_state.sub_page:
    
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
                st.title(name)
                col1_1, col1_2 = st.columns([2, 1])
                with col1_1:
                    st.image("image\s_img.jpg", width=270)
                with col1_2:
                    st.subheader("나의 인적사항")
                    st.write("학년: 6학년")
                    st.write("나이: 12세")
                    st.write("특이사항: 청각장애 4급1호")
                    st.write("주소: 대구광역시 중구")
                    st.write("학생 연락처: 010-1234-5678")
                    st.write("부모 연락처: 010-1234-5678")
                    
                score_plot('student_data.csv', '최수아')
                radar_plot('student_data.csv', '최수아')

            with col2:
                ai_chatbot.main()
        
        
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
    else:
        sub_page.main()