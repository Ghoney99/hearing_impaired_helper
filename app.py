import streamlit as st
from utils import get_session_state
import main_page
import pandas as pd

#####################################################################
# 제목 : 시작 앱
# 수정 날짜 : 2024-07-01
# 작성자 : 장재혁
# 수정자 : 장재혁
# 수정 내용 : 시작앱 파일 생성
#####################################################################

# 세션 상태를 가져오기
if 'main_page' not in st.session_state:
    st.session_state.main_page = False
if 'student_name' not in st.session_state:
    st.session_state.student_name = None

if not st.session_state.main_page:
    # 초기 페이지: 버튼 표시
    st.title("VONDI")
    
    # 데이터셋 로드
    df = pd.read_csv('student_data.csv')
    
    # Name과 StudentID를 매핑
    name_to_student_id = dict(zip(df['Name'], df['StudentID']))
    
    # 학생 이름 입력
    student_name = st.text_input('이름:')
    student_pw = st.text_input('비밀번호:', type="password")
    
    if st.button('확인'):
        if student_name in name_to_student_id:
            # 세션 상태에 학생 이름과 ID 저장
            st.session_state.student_name = student_name
            st.session_state.student_id = name_to_student_id[student_name]
            st.session_state.main_page = True
            st.experimental_rerun()  # 페이지 리로드
        else:
            st.write("이름 또는 비밀번호가 잘못되었습니다.")
else:
    # 메인 페이지로 이동
    main_page.main(st.session_state.student_name)