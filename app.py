import streamlit as st
from utils import get_session_state
import main_page
import teacher_page
import admin_page  # 관리자 페이지를 위한 모듈 (생성 필요)
import pandas as pd

#####################################################################
# 제목 : 시작 앱
# 수정 날짜 : 2024-07-01
# 작성자 : 장재혁
# 수정자 : 장지헌, Assistant
# 수정 내용 : 학생/선생님/관리자 구분 추가
#####################################################################

# 세션 상태를 가져오기
if 'main_page' not in st.session_state:
    st.session_state.main_page = False
if 'student_name' not in st.session_state:
    st.session_state.student_name = None
if 'user_type' not in st.session_state:
    st.session_state.user_type = None

if not st.session_state.main_page:
    # 초기 페이지: 버튼 표시
    st.image('image\logo.png')

    # 데이터셋 로드
    df = pd.read_csv('datasets/student_data.csv')

    # Name과 StudentID를 매핑
    name_to_student_id = dict(zip(df['Name'], df['StudentID']))

    # 사용자 유형 선택
    user_type = st.radio("사용자 유형을 선택하세요:", ("학생", "선생님", "관리자"))

    # 이름 입력
    name = st.text_input('이름:')
    password = st.text_input('비밀번호:', type="password")

    if st.button('확인'):
        if user_type == "학생":
            if name in name_to_student_id:
                # 세션 상태에 학생 이름과 ID 저장
                st.session_state.student_name = name
                st.session_state.student_id = name_to_student_id[name]
                st.session_state.main_page = True
                st.session_state.user_type = "학생"
                st.experimental_rerun()  # 페이지 리로드
            else:
                st.write("이름 또는 비밀번호가 잘못되었습니다.")
        elif user_type == "선생님":
            if name == "선생님" and password == "1234":  # 임시 검증
                st.session_state.teacher_name = name
                st.session_state.main_page = True
                st.session_state.user_type = "선생님"
                st.experimental_rerun()  # 페이지 리로드
            else:
                st.write("이름 또는 비밀번호가 잘못되었습니다.")
        else:  # 관리자인 경우
            if name == "관리자" and password == "1234":  # 임시 검증
                st.session_state.admin_name = name
                st.session_state.main_page = True
                st.session_state.user_type = "관리자"
                st.experimental_rerun()  # 페이지 리로드
            else:
                st.write("이름 또는 비밀번호가 잘못되었습니다.")
else:
    # 메인 페이지, 선생님 페이지 또는 관리자 페이지로 이동
    if st.session_state.user_type == "학생":
        main_page.main(st.session_state.student_name)
    elif st.session_state.user_type == "선생님":
        teacher_page.main(st.session_state.teacher_name)
    elif st.session_state.user_type == "관리자":
        admin_page.main(st.session_state.admin_name)