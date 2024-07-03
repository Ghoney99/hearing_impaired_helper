import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from streamlit_calendar import calendar  # Assuming this library is correctly installed
import sub_page  # Assuming sub_page module is defined
import ai_chatbot  # Assuming ai_chatbot module is defined

# Set font family for matplotlib plots
plt.rcParams['font.family'] = 'Malgun Gothic'

def score_plot(df, student_name):
    st.subheader('학년별 성적 조회')
    # Your existing score_plot function implementation

def radar_plot(df, student_name):
    st.subheader('방사형 성적 그래프')
    # Your existing radar_plot function implementation

def digital_textbook():
    st.title("디지털 교과서")
    st.write("디지털 교과서 내용을 여기에 추가하세요.")
    # Add more content related to digital textbooks here

def academic_calendar():
    st.title("에이블 초등학교 학사 일정")
    calendar_events = [
        {"title": "방학", "start": "2024-07-31"},
        {"title": "기말고사", "start": "2024-07-30"}
    ]
    calendar = calendar(events=calendar_events)
    st.write(calendar)

def learning_progress():
    st.title("학습 현황")
    # Generate random learning progress data
    learning_data = {
        '과목': ['국어', '수학', '영어', '과학', '사회'],
        '진도': [75, 80, 60, 90, 70]  # Random progress data for each subject
    }

    # Create DataFrame
    df_learning = pd.DataFrame(learning_data)

    # Set font for plots
    plt.rcParams['font.family'] = 'Malgun Gothic'

    # Draw doughnut charts for learning progress
    st.write("과목별 진도 현황")
    num_charts_per_row = 3
    num_subjects = len(df_learning)
    num_rows = (num_subjects + num_charts_per_row - 1) // num_charts_per_row

    fig, axs = plt.subplots(num_rows, num_charts_per_row, figsize=(15, 5 * num_rows))

    for i, ax in enumerate(axs.flat):
        if i < num_subjects:
            subject = df_learning.loc[i, '과목']
            progress = df_learning.loc[i, '진도']

            # Draw doughnut chart
            wedges, texts, autotexts = ax.pie([progress, 100 - progress], colors=['blue', 'white'], startangle=90,
                                              wedgeprops=dict(width=0.3), autopct='%1.1f%%',
                                              textprops={'fontsize': 14, 'color': 'black'})

            # Place percentage value (progress percentage) in the center
            centre_circle = plt.Circle((0, 0), 0.70, color='white', fc='white', linewidth=1.25)
            ax.add_artist(centre_circle)

            # Set title
            ax.set_title(f'{subject} 진도', fontsize=16)

            # Hide autotexts for empty sections
            for autotext in autotexts:
                if autotext.get_text() == '':
                    autotext.set_visible(False)

        else:
            # Draw empty chart in remaining space
            ax.axis('off')

    # Display doughnut charts in card format
    st.write("---")
    cols = st.columns(1)
    with cols[0]:
        st.pyplot(fig)

def student_performance(df):
    st.title("학생 성적 조회 대시보드")
    selected_student = st.selectbox("학생 선택", df['Name'].unique())

    # Display selected student's scores and radar chart
    if selected_student:
        score_plot(df, selected_student)
        radar_plot(df, selected_student)

def main(name):
    # Set page configuration
    st.set_page_config(layout="wide")

    # Sidebar menu options
    with st.sidebar:
        choose = st.radio("메뉴 선택", ['마이페이지', '교과서', '디지털 교과서', '학사 일정', '학습 현황', '학생 성적'], index=0)

    # Handle menu options
    if choose == '마이페이지':
        col1, col2 = st.columns([2, 1])

        with col1:
            st.title(name)
            st.write("성적 확인")
            score_plot('student_data.csv', '최수아')
            radar_plot('student_data.csv', '최수아')

        with col2:
            ai_chatbot.main()

    elif choose == '교과서':
        col1, col2, col3 = st.columns(3)

        with col1:
            st.image("image/국어표지1.png", caption="국어")
            st.text("국어")
            if st.button("국어"):
                st.experimental_rerun()  # Page reload
                # Add functionality for "국어" button action here

        with col2:
            st.image("image/수학표지1.png", caption="수학")
            st.text("수학")
            if st.button("수학"):
                st.write("수학 버튼을 눌렀습니다.")

        with col3:
            st.image("image/영어표지1.jpg", caption="영어")
            st.text("영어")
            if st.button("영어"):
                st.write("영어 버튼을 눌렀습니다.")

    elif choose == '디지털 교과서':
        digital_textbook()

    elif choose == '학사 일정':
        academic_calendar()

    elif choose == '학습 현황':
        learning_progress()

    elif choose == '학생 성적':
        student_performance(pd.read_csv('student_data.csv'))

    else:
        st.write("구현되지 않은 기능입니다.")

# Example usage
if __name__ == '__main__':
    main("사용자 이름")
