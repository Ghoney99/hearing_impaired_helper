import streamlit as st
from utils import get_session_state
import main_page
import teacher_page  # 선생님 페이지를 위한 모듈 (아직 없다면 생성해야 합니다)
import pandas as pd

#####################################################################
# 제목 : 시작 앱
# 수정 날짜 : 2024-07-01
# 작성자 : 장재혁
# 수정자 : 장지헌
# 수정 내용 : 학생/선생님 구분 추가
#####################################################################

# 세션 상태를 가져오기
if 'main_page' not in st.session_state:
    st.session_state.main_page = False
if 'student_name' not in st.session_state:
    st.session_state.student_name = None
if 'is_teacher' not in st.session_state:
    st.session_state.is_teacher = False

if not st.session_state.main_page:
    # 초기 페이지: 버튼 표시
    st.title("VONDI")

    # 데이터셋 로드
    df = pd.read_csv('student_data.csv')

    # Name과 StudentID를 매핑
    name_to_student_id = dict(zip(df['Name'], df['StudentID']))

    # 사용자 유형 선택
    user_type = st.radio("사용자 유형을 선택하세요:", ("학생", "선생님"))

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
                st.session_state.is_teacher = False
                st.experimental_rerun()  # 페이지 리로드
            else:
                st.write("이름 또는 비밀번호가 잘못되었습니다.")
        else:  # 선생님인 경우
            # 여기에 선생님 인증 로직을 추가해야 합니다.
            # 이 예제에서는 간단히 처리합니다.
            if name == "선생" and password == "1234":  # 임시 검증
                st.session_state.teacher_name = name
                st.session_state.main_page = True
                st.session_state.is_teacher = True
                st.experimental_rerun()  # 페이지 리로드
            else:
                st.write("이름 또는 비밀번호가 잘못되었습니다.")
else:
    # 메인 페이지 또는 선생님 페이지로 이동
    if st.session_state.is_teacher:
        teacher_page.main(st.session_state.teacher_name)
    else:
        main_page.main(st.session_state.student_name)