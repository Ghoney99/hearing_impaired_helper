import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 경로
file_path = 'student_data.csv'

# Streamlit 애플리케이션 설정
def score_plot():
    st.title('학년별 성적 조회')

    # 데이터 로드
    df = pd.read_csv(file_path)

    # 학생 이름 선택
    student_name = '최수아'

    # 선택한 학생 데이터 필터링
    filtered_data = df[df['Name'] == student_name]

    # 학년 선택
    grade = st.slider('학년 선택:', min_value=1, max_value=6, value=(1, 6))

    # 선택된 데이터 필터링
    filtered_data = filtered_data[(filtered_data['Grade'].between(grade[0], grade[1]))]

    # 과목 체크박스 생성 (국어 기본 선택)
    default_subjects = ['국어']
    subjects = st.multiselect('과목 선택:', filtered_data['Subject'].unique(), default=default_subjects)

    # 그래프 그리기
    if not filtered_data.empty:
        plt.figure(figsize=(10, 6))
        for subject in subjects:
            subject_data = filtered_data[filtered_data['Subject'] == subject]
            plt.plot(subject_data['Total_Semester'], subject_data['Score'], marker='o', label=subject)
        plt.xlabel('학기')
        plt.ylabel('성적')
        plt.title(f'{student_name}학생의 {grade[0]} ~ {grade[1]} 학년 성적')
        plt.legend()
        st.pyplot(plt)

if __name__ == '__main__':
    score_plot()
