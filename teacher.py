import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from streamlit_calendar import calendar # 라이브러리 설치

# 글꼴 설정
plt.rcParams['font.family'] ='Malgun Gothic'

def score_plot(df, student_name):
    st.subheader('학년별 성적 조회')

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

def radar_plot(df, student_name):
    st.subheader('방사형 성적 그래프')

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

# CSV 파일 읽기
data = pd.read_csv('student_data.csv')

# 캘린더
st.title("에이블 초등학교 학사 일정")
calendar_events = [
    {
        "title": "방학",
        "start": "2024-07-31",

    },
    {
        "title": "기말고사",
        "start": "2024-07-30",
    }
]
calendar = calendar(events=calendar_events)

# 사이드바에 버튼 추가
st.sidebar.header("디지털 교과서 - 교사용")

if st.sidebar.button("학습현황"):
    # 임의의 학습 진도 데이터 생성
    learning_data = {
        '과목': ['국어', '수학', '영어', '과학', '사회'],
        '진도': [75, 80, 60, 90, 70]  # 각 과목의 진도 (임의의 데이터)
    }

    # DataFrame 생성
    df_learning = pd.DataFrame(learning_data)

    # 글꼴 설정
    plt.rcParams['font.family'] = 'Malgun Gothic'

    # 학습현황 도넛 차트 그리기
    st.title("학습현황")
    st.write("과목별 진도 현황")

    # 3개씩 도넛 차트를 나열하기 위해 반복문 사용
    num_charts_per_row = 3
    num_subjects = len(df_learning)
    num_rows = (num_subjects + num_charts_per_row - 1) // num_charts_per_row

    fig, axs = plt.subplots(num_rows, num_charts_per_row, figsize=(15, 5 * num_rows))

    for i, ax in enumerate(axs.flat):
        if i < num_subjects:
            subject = df_learning.loc[i, '과목']
            progress = df_learning.loc[i, '진도']
            
            # 도넛 차트 그리기
            wedges, texts, autotexts = ax.pie([progress, 100 - progress], colors=['blue', 'white'], startangle=90, wedgeprops=dict(width=0.3), autopct='%1.1f%%', textprops={'fontsize': 14, 'color': 'black'})

            # 중앙에 값(진도의 백분율) 위치시키기
            centre_circle = plt.Circle((0, 0), 0.70, color='white', fc='white', linewidth=1.25)
            ax.add_artist(centre_circle)
            
            # 제목 설정
            ax.set_title(f'{subject} 진도', fontsize=16)

            # autotexts 중 빈 부분은 숨기기
            for autotext in autotexts:
                if autotext.get_text() == '':
                    autotext.set_visible(False)

        else:
            # 남는 공간에 빈 그래프 그리기
            ax.axis('off')

    # 도넛 차트를 카드 형태로 만들기
    st.write("---")
    cols = st.columns(1)
    with cols[0]:
        st.pyplot(fig)

if st.sidebar.button("학생성적"):
    st.title("학생 성적 조회 대시보드")
    selected_student = st.selectbox("학생 선택", data['Name'].unique())

    # 선택된 학생에 대한 성적 조회 및 방사형 그래프 생성
    if selected_student:
        score_plot(data, selected_student)
        radar_plot(data, selected_student)
        
if st.sidebar.button("디지털 교과서"):
    ## 여기에 추가해줘
    # 세 개의 컬럼 만들기
    col1, col2, col3 = st.columns(3)

    # 첫 번째 컬럼에 이미지와 텍스트, 버튼 추가
    with col1:
        st.image("image\국어표지1.png", caption="국어")
        st.text("국어")
        if st.button("국어"):
            # session_state.sub_page = True
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