import streamlit as st
from utils import get_session_state
import main_page
import pandas as pd

# 세션 상태 가져오기
session_state = get_session_state(main_page=False)

if not session_state.main_page:
    
    # 초기 페이지: 버튼 표시
    st.title("VONDI")
    # 데이터셋 로드
    df = pd.read_csv('student_scores_korean_subjects.csv')

    # 학생 이름과 ID를 매핑
    student_name_to_id = {row['이름']: row['학생ID'] for _, row in df.iterrows()}
    # 학생 아이디 입력
    
    student_id = st.text_input('ID:')
    student_pw = st.text_input('Password:', type="password")

    

    if st.button('확인'):
        if student_id in student_name_to_id:
            # 페이지 이동
            session_state.main_page = True
            st.experimental_rerun()  # 페이지 리로드
        else:
            st.write("아이디 또는 비밀번호가 잘못되었습니다.")
else:
    # 메인 페이지로 이동
    main_page.main()
