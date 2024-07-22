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

# #####################################################################
# # 제목 : 메인 페이지
# # 수정 날짜 : 2024-07-10
# # 작성자 : 장재혁
# # 수정자 : 장지헌
# # 수정 내용 : 사이드바 제목 수정 및 기능 추가
# #####################################################################

# 파일불러오기
import sub_page, ai_chatbot, background

# 페이지 전환
from utils import get_session_state


# 글꼴 설정
plt.rcParams['font.family'] ='Malgun Gothic'

def score_plot(file_path, s_name):
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


# def radar_plot(file_path, student_name):
#     # 데이터 읽기
#     df = pd.read_csv(file_path)

#     # 학생 데이터 필터링
#     student_data = df[df['Name'] == student_name]

#     # 학년 및 학기 선택 옵션 생성
#     unique_grades = student_data['Grade'].unique()
#     unique_semesters = student_data['Semester'].unique()

#     # 학년 및 학기 선택
#     selected_grade = st.selectbox(f"{student_name} 학생의 학년", unique_grades)
#     selected_semester = st.selectbox(f"{selected_grade}학년 학기", unique_semesters)

#     # 선택한 학년 및 학기의 데이터 필터링
#     filtered_data = student_data[(student_data['Grade'] == selected_grade) & (student_data['Semester'] == selected_semester)]

#     # 방사형 그래프 생성
#     if not filtered_data.empty:
#         subjects = filtered_data['Subject'].unique()
#         scores = [filtered_data[filtered_data['Subject'] == subject]['Score'].values[0] for subject in subjects]

#         fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
#         ax.set_theta_zero_location("N")
#         ax.set_theta_direction(-1)
#         ax.set_rlim(0, 100)
#         ax.set_thetagrids(np.arange(0, 360, 360 / len(subjects)), subjects)
#         ax.plot(np.radians(np.arange(0, 360, 360 / len(subjects))), scores, 'o', color='blue', alpha=0.7)
#         ax.fill(np.radians(np.arange(0, 360, 360 / len(subjects))), scores, alpha=0.2)
#         ax.set_title(f"{student_name} 학생의 {selected_grade}학년 {selected_semester}학기 성적")

#         st.pyplot(fig)
#     else:
#         st.write("해당 학년 및 학기의 데이터가 없습니다.")


def main(name):
    #오류나서 주석처리
    #st.set_page_config(layout="wide")
    session_state = get_session_state(sub_page=False)
    
    if session_state.sub_page:
        sub_page.main()
    else:
        with st.sidebar:
            st.image('image\logo.png')
            choose = option_menu(
                menu_title=None,
                options=['마이페이지', "교과서"],
                icons=['house', 'bi bi-journals'],
                menu_icon="app-indicator", 
                default_index=0,
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
                }
            )

        # 상단 바 - 주석처리
        # col1, col2, col3 = st.columns([1,6,1])
        # with col1:
        #     st.write(f"# {name} 😊")
        # with col2:
        #     st.text_input("검색하세요", placeholder="검색어를 입력하세요")
        # with col3:
        #     st.button("🔔")

    ############################################################################################################ 
    # 마이페이지
    ############################################################################################################  
        if choose == "마이페이지":
            background.add_bg_from_url2()
            # 주석처리
            # col1, col2, col3 = st.columns(3)
            
            # with col1:
            #     # 학년별 성적 조회
            #     st.subheader("학년별 성적 조회")
            #     score_plot('datasets/student_data.csv', name)

            # with col2:
            #     # 부족한 과목 분석
            #     st.subheader("부족한 과목 분석")
            #     fig, ax = plt.subplots()
            #     size = 0.3
            #     vals = [40, 35, 25]
            #     ax.pie(vals, labels=['국어', '수학', '과학'], radius=1, wedgeprops=dict(width=size, edgecolor='white'), colors=['#4e73df', '#1cc88a', '#36b9cc'])
            #     ax.text(0, 0, "전과목", ha='center', va='center', fontsize=16)
            #     st.pyplot(fig)

            # with col3:
            #             # 선생님 1:1 문의
            #             st.subheader("선생님 1:1 문의")
            #             teachers = ['국어 선생님', '수학 선생님', '과학 선생님']
            #             for teacher in teachers:
            #                 st.write(f"👩‍🏫 {teacher}")

            #             # 오늘의 할 일 (선생님 1:1 문의 아래에 배치)
            #             st.subheader("오늘의 할 일")
            #             tasks = [
            #                 "4/24 발표대회 주제 정하기",
            #                 "4/24 발표대회 주제 정하기",
            #                 "4/24 발표대회 주제 정하기",
            #                 "4/24 발표대회 주제 정하기",
            #                 "4/26 발표대회 주제 정하기"
            #             ]
            #             for i, task in enumerate(tasks):
            #                 if i < 2:
            #                     st.write(f"✅ {task}")
            #                 elif i < 4:
            #                     st.write(f"⭐ {task}")
            #                 else:
            #                     st.write(f"🌟 {task}")

            #             # 공지사항 (오늘의 할 일 아래에 배치)
            #             st.subheader("공지사항")
            #             notices = [
            #                 "5/1 어린이날 행사 안내",
            #                 "5/10 학부모 상담 주간",
            #                 "5/15 봄 소풍 예정"
            #             ]
            #             for notice in notices:
            #                 st.write(f"📢 {notice}")

            # col4, col5, col6 = st.columns(3)

            # with col4:
            #     # 과목별 부족한 유형 분석
            #     st.subheader("과목별 부족한 유형 분석")
            #     subjects_data = {
            #         "국어": {"글쓰기": 41, "말하기": 46, "독해": 13},
            #         "수학": {"공간기하": 47, "논리력": 16, "분수": 37},
            #         "과학": {"탐구력": 44, "과학실험": 20, "주제력": 36}
            #     }
                
            #     subject_cols = st.columns(3)
            #     for i, (subject, data) in enumerate(subjects_data.items()):
            #         with subject_cols[i]:
            #             st.write(f"### {subject}")
            #             fig, ax = plt.subplots(figsize=(3, 3))  # 그래프 크기 조정
            #             colors = ['#8e5ea2', '#3cba9f', '#e8c3b9']
            #             ax.pie(data.values(), labels=data.keys(), colors=colors, autopct='%1.1f%%')
            #             st.pyplot(fig)

            # with col5:
            #     # 작년 성적과 현 학년 성적 비교
            #     st.subheader("학년별 과목 성적 비교")
            #     comparison_fig = compare_grades('datasets/student_data.csv', name)
            #     st.pyplot(comparison_fig)

            # with col6:
            #     pass

    ############################################################################################################ 
    # 교과서
    ############################################################################################################       
        elif choose == "교과서": 
            background.add_bg_from_url3()
            
            st.title('')
            st.title('')
            st.title('')
            st.text('')
            st.text('')
            empty, con1, con2, con3 = st.columns([0.12,0.11,0.11,0.15])
            with empty:
                pass
            with con1:
                if st.button("국어"):
                    session_state.sub_page = True
                    st.experimental_rerun()  # 페이지 리로드
            with con2:
                st.button("수학")
            with con3:
                st.button("수학익힘")
            # 주석처리
            # info_col1, info_col2, info_col3 = st.columns(3)
            # with info_col1:
            #     st.markdown("""
            #     <div style='background-color: #e6ffe6; padding: 10px; border-radius: 10px;'>
            #         <h3 style='color: green;'>✏️ 국어</h3>
            #         <p>▲ 수업시간: 금요일 2교시</p>
            #     </div>
            #     """, unsafe_allow_html=True)
            # with info_col2:
            #     st.markdown("""
            #     <div style='background-color: #e6f3ff; padding: 10px; border-radius: 10px;'>
            #         <h3 style='color: blue;'>📋 받아쓰기</h3>
            #         <p>▲ 4월 26일까지</p>
            #     </div>
            #     """, unsafe_allow_html=True)
            # with info_col3:
            #     st.markdown("""
            #     <div style='background-color: #ffe6f3; padding: 10px; border-radius: 10px;'>
            #         <h3 style='color: purple;'>📅 운동회</h3>
            #         <p>▲ 4월 30일</p>
            #     </div>
            #     """, unsafe_allow_html=True)
                
            # # 세 개의 컬럼 만들기
            # col1, col2, col3 = st.columns(3)

            # # 첫 번째 컬럼에 이미지와 텍스트, 버튼 추가
            # with col1:
            #     st.image("image\국어표지1.png", caption="국어")
            #     st.text("국어")
            #     if st.button("국어"):
            #         session_state.sub_page = True
            #         st.experimental_rerun()  # 페이지 리로드

            # # 두 번째 컬럼에 이미지와 텍스트, 버튼 추가
            # with col2:
            #     st.image("image\수학표지1.png", caption="수학")
            #     st.text("수학")
            #     if st.button("수학"):
            #         st.write("수학 버튼을 눌렀습니다.")

            # # 세 번째 컬럼에 이미지와 텍스트, 버튼 추가
            # with col3:
            #     st.image("image\영어표지1.jpg", caption="영어")
            #     st.text("영어")
            #     if st.button("영어"):
            #         st.write("영어 버튼을 눌렀습니다.")
        else:
            sub_page.main()

        if session_state.sub_page:
            sub_page.main()
