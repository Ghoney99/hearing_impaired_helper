import streamlit as st
from utils import get_session_state
import main_page

# 세션 상태 가져오기
session_state = get_session_state(main_page=False)

if not session_state.main_page:
    # 초기 페이지: 버튼 표시
    st.title("Welcome to My App")
    if st.button("Go to Main Page"):
        session_state.main_page = True
        st.experimental_rerun()  # 페이지 리로드
else:
    # 메인 페이지로 이동
    main_page.main()
