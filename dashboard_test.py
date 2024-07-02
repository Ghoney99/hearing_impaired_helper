import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

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


# Streamlit 앱 실행
st.title("학생 성적 조회")
file_path = st.text_input("CSV 파일 경로", "student_data.csv")
student_name = st.text_input("학생 이름", "최수아")
plot_radar_chart(file_path, student_name)
