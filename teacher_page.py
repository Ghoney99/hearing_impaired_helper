import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from streamlit_option_menu import option_menu
from streamlit_calendar import calendar

# #####################################################################
# # 제목 : 선생님 페이지
# # 수정 날짜 : 2024-07-01
# # 작성자 : 장지헌
# # 수정자 : 장지헌
# # 수정 내용 : .. 수정중
# #####################################################################

plt.rcParams['font.family'] = 'Malgun Gothic'

st.set_page_config(layout="wide")

def score_plot(file_path, student_name):
    st.title(f'{student_name}의 학년별 성적 조회')

    df = pd.read_csv(file_path)

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
        plt.title(f'{student_name} 학생의 {grade[0]} ~ {grade[1]} 학년 성적')
        plt.legend()
        st.pyplot(plt)

def compare_grades(file_path, student_name):
    # 데이터 로드
    df = pd.read_csv(file_path)
    
    # 학생 데이터 필터링
    student_data = df[df['Name'] == student_name]
    
    # 현재 학년과 이전 학년 구하기
    current_grade = student_data['Grade'].max()
    previous_grade = current_grade - 1
    
    # 현재 학년과 이전 학년 데이터 추출
    current_data = student_data[student_data['Grade'] == current_grade].groupby('Subject')['Score'].mean()
    previous_data = student_data[student_data['Grade'] == previous_grade].groupby('Subject')['Score'].mean()
    
    # 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = range(len(current_data))
    width = 0.35
    
    ax.bar([i - width/2 for i in x], previous_data, width, label=f'{previous_grade}학년', alpha=0.8)
    ax.bar([i + width/2 for i in x], current_data, width, label=f'{current_grade}학년', alpha=0.8)
    
    ax.set_ylabel('평균 점수')
    ax.set_title(f'{student_name}의 학년별 과목 성적 비교')
    ax.set_xticks(x)
    ax.set_xticklabels(current_data.index)
    ax.legend()
    
    plt.tight_layout()
    return fig


def main(teacher_name):
    st.title(f"선생님 대시보드 - {teacher_name}")

    # CSV 파일 읽기
    file_path = 'datasets/student_data.csv'
    df = pd.read_csv(file_path)

    with st.sidebar:
        choose = option_menu("메뉴", ["학생 관리", "성적 관리", "학사 일정", "학습 진도"],
                             icons=['bi bi-people', 'bi bi-graph-up', 'bi bi-calendar', 'bi bi-book'],
                             default_index=0,
                             styles={
                                 "container": {"padding": "5!important", "background-color": "#fafafa"},
                                 "icon": {"color": "orange", "font-size": "25px"},
                                 "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                                 "nav-link-selected": {"background-color": "#02ab21"},
                             })

    # 학생 선택
    selected_student = st.selectbox("학생 선택", df['Name'].unique())

    if choose == "학생 관리":
        st.header("학생 정보")
        if selected_student:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image("image\s_img.jpg", width=200)
            with col2:
                st.subheader(f"{selected_student}의 인적사항")
                st.write("이름: ", selected_student)
                st.write("학년: 6학년")
                st.write("나이: 12세")
                st.write("특이사항: 청각장애 4급1호")
                st.write("주소: 대구광역시 중구")
                st.write("학생 연락처: 010-1234-5678")
                st.write("부모 연락처: 010-1234-5678")
            
            st.image("image\청각장애 등급.png", width=600)

    elif choose == "성적 관리":
            st.header("성적 관리")
            if selected_student:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.subheader("학년별 성적 조회")
                    score_plot(file_path, selected_student)

                with col2:
                    st.subheader("부족한 과목 분석")
                    fig, ax = plt.subplots()
                    size = 0.3
                    vals = [40, 35, 25]
                    ax.pie(vals, labels=['국어', '수학', '과학'], radius=1, wedgeprops=dict(width=size, edgecolor='white'), colors=['#4e73df', '#1cc88a', '#36b9cc'])
                    ax.text(0, 0, "전과목", ha='center', va='center', fontsize=16)
                    st.pyplot(fig)

                with col3:
                    st.subheader("선생님 1:1 문의")
                    teachers = ['국어 선생님', '수학 선생님', '과학 선생님']
                    for teacher in teachers:
                        st.write(f"👩‍🏫 {teacher}")

                    st.subheader("오늘의 할 일")
                    tasks = [
                        "4/24 발표대회 주제 정하기",
                        "4/24 발표대회 주제 정하기",
                        "4/26 발표대회 주제 정하기"
                    ]
                    for i, task in enumerate(tasks):
                        if i < 2:
                            st.write(f"✅ {task}")
                        else:
                            st.write(f"🌟 {task}")

                    st.subheader("공지사항")
                    notices = [
                        "5/1 어린이날 행사 안내",
                        "5/10 학부모 상담 주간",
                        "5/15 봄 소풍 예정"
                    ]
                    for notice in notices:
                        st.write(f"📢 {notice}")

                col4, col5, col6 = st.columns(3)

                with col4:
                    st.subheader("과목별 부족한 유형 분석")
                    subjects_data = {
                        "국어": {"글쓰기": 41, "말하기": 46, "독해": 13},
                        "수학": {"공간기하": 47, "논리력": 16, "분수": 37},
                        "과학": {"탐구력": 44, "과학실험": 20, "주제력": 36}
                    }
                    
                    subject_cols = st.columns(3)
                    for i, (subject, data) in enumerate(subjects_data.items()):
                        with subject_cols[i]:
                            st.write(f"### {subject}")
                            fig, ax = plt.subplots(figsize=(3, 3))
                            colors = ['#8e5ea2', '#3cba9f', '#e8c3b9']
                            ax.pie(data.values(), labels=data.keys(), colors=colors, autopct='%1.1f%%')
                            st.pyplot(fig)

                with col5:
                    st.subheader("학년별 과목 성적 비교")
                    comparison_fig = compare_grades(file_path, selected_student)
                    st.pyplot(comparison_fig)

                with col6:
                    pass
                
    elif choose == "학사 일정":
        st.header("에이블 초등학교 학사 일정")
        calendar_events = [
            {"title": "기말고사", "start": "2024-07-30"},
            {"title": "방학", "start": "2024-07-31"}
        ]
        calendar(events=calendar_events)

    elif choose == "학습 진도":
        st.header("학습 진도")
        if selected_student:
            learning_data = {
                '과목': ['국어', '수학', '영어', '과학', '사회'],
                '진도': [74.1, 85.4, 67.5, 90, 77.5]
            }
            df_learning = pd.DataFrame(learning_data)

            st.write(f"{selected_student} 학생의 학습 진도")
            st.dataframe(df_learning)

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(df_learning['과목'], df_learning['진도'])
            ax.set_ylim(0, 100)
            ax.set_ylabel('진도 (%)')
            ax.set_title(f'{selected_student} 학생의 과목별 학습 진도')
            st.pyplot(fig)

            st.write("학습 진도 분석:")
            st.write("영어와 사회 과목의 진도가 타 과목들에 비해 뒤처지고 있습니다. 추가적인 학습 시간 배정과 보충 수업을 고려해볼 필요가 있습니다.")
