import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from streamlit_option_menu import option_menu
from streamlit_calendar import calendar # 라이브러리 설치

# Set font family for matplotlib plots
plt.rcParams['font.family'] = 'Malgun Gothic'

st.set_page_config(layout="wide")

# 스트림릿 테마 선택



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

def main():
    # CSV 파일 읽기
    file_path = 'student_data.csv'
    df = pd.read_csv(file_path)

    with st.sidebar:
        choose = option_menu("메뉴", ["학생 성적", "디지털 교과서", "학사 일정", "학습 현황"],
                             icons=['bi bi-bar-chart', 'bi bi-book', 'bi bi-calendar', 'bi bi-bookmark'],
                             default_index=0,
                             styles={
                                 "container": {"padding": "5!important", "background-color": "#fafafa"},
                                 "icon": {"color": "orange", "font-size": "25px"},
                                 "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                                 "nav-link-selected": {"background-color": "#02ab21"},
                             })

    if choose == "학생 성적":
        st.title("학생 성적 조회 대시보드")
        selected_student = st.selectbox("학생 선택", df['Name'].unique())

        if selected_student:
            col1, col2 = st.columns([1, 1])

            # 1. 학생 이미지
            # 1. 학생 이미지 (크기 조절)
            with col1:
                col1_1, col1_2 = st.columns([1, 1])
                with col1_1:
                    st.image("image\s_img.jpg", width=270)
                with col1_2:
                    st.subheader(f"{selected_student}의 인적사항")
                    st.write("이름: ", selected_student)
                    st.write("학년: 6학년")
                    st.write("나이: 12세")
                    st.write("특이사항: 청각장애 4급1호")
                    st.write("주소: 대구광역시 중구")
                    st.write("학생 연락처: 010-1234-5678")
                    st.write("부모 연락처: 010-1234-5678")
                ####
                # 내용을 추가하고 싶어
                st.image("image\청각장애 등급.png", width=600)
                ####
                
            # 2. Radar plot
            with col2:
                radar_plot(file_path, selected_student)

            st.write("---")

            # 4. Score plot
            score_plot(file_path, selected_student)

    elif choose == "디지털 교과서":
        st.title("디지털 교과서")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.image("image/국어표지1.png", caption="국어")
            if st.button("국어"):
                st.write("국어 버튼을 눌렀습니다.")

        with col2:
            st.image("image/수학표지1.png", caption="수학")
            if st.button("수학"):
                st.write("수학 버튼을 눌렀습니다.")

        with col3:
            st.image("image/영어표지1.jpg", caption="영어")
            if st.button("영어"):
                st.write("영어 버튼을 눌렀습니다.")

    elif choose == "학사 일정":
        st.title("에이블 초등학교 학사 일정")
        
        calendar_events = [
            {
                "title": "기말고사",
                "start": "2024-07-30",
            },
            {
                "title": "방학",
                "start": "2024-07-31",
            }
        ]

        calendar(events=calendar_events)

    elif choose == "학습 현황":
        st.title("학습 현황")
        learning_data = {
            '과목': ['국어', '수학', '영어', '과학', '사회'],
            '진도': [74.1, 85.4, 67.5, 90, 77.5]
        }
        df_learning = pd.DataFrame(learning_data)

        st.header("영어와 사회 과목의 진도가 타 과목들에 비해서 많이 뒤처지고 있어서 학습 계획을 재조정할 필요가 있습니다. \n영어와 사회 과목 모두 중요한 과목이기 때문에, 이러한 상황을 개선하기 위해 추가적인 학습 시간을 배정하고, 필요한 경우에는 보충 수업을 진행하는 것도 고려해 볼 필요가 있습니다.\n특히, 영어 과목의 경우 문법과 어휘, 독해 능력 향상을 위한 추가적인 연습이 필요하며, 사회 과목의 경우 다양한 역사적 사건과 사회적 이슈에 대한 깊이 있는 이해를 돕기 위한 자료를 제공하는 것이 중요합니다. 이러한 조치들을 통해 두 과목의 학습 진도를 다른 과목들과 균형 있게 맞춰 나가도록 노력해야 합니다.")
        num_charts_per_row = 3
        num_subjects = len(df_learning)
        num_rows = (num_subjects + num_charts_per_row - 1) // num_charts_per_row

        fig, axs = plt.subplots(num_rows, num_charts_per_row, figsize=(15, 5 * num_rows))

        for i, ax in enumerate(axs.flat):
            if i < num_subjects:
                subject = df_learning.loc[i, '과목']
                progress = df_learning.loc[i, '진도']
                wedges, texts, autotexts = ax.pie(
                    [progress, 100 - progress],
                    colors=['blue', 'white'],
                    startangle=90,
                    wedgeprops=dict(width=0.3),
                    autopct='%1.1f%%',
                    textprops={'fontsize': 14, 'color': 'black'}
                )

                centre_circle = plt.Circle((0, 0), 0.70, color='white', fc='white', linewidth=1.25)
                ax.add_artist(centre_circle)
                ax.set_title(f'{subject} 진도', fontsize=16)
                for autotext in autotexts:
                    if autotext.get_text() == '':
                        autotext.set_visible(False)

            else:
                ax.axis('off')

        st.write("---")
        cols = st.columns(1)
        with cols[0]:
            st.pyplot(fig)

if __name__ == "__main__":
    main()
