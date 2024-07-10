import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from streamlit_option_menu import option_menu

#####################################################################
# 제목 : 관리자 페이지
# 수정 날짜 : 2024-07-10
# 작성자 : 장지헌
# 수정자 : 장지헌
# 수정 내용 : 관리자 페이지 완성
#####################################################################

def main(admin_name):
    st.sidebar.title(f"환영합니다, {admin_name}")
    
    with st.sidebar:
        choose = option_menu("VONDI", 
                             ['종합', '서버 및 시스템', 'DB 관리', 'API 사용량', '보안 현황', '사용자 관리', '로그 분석'],
                             icons=['house', 'graph-up', 'pc-display', 'database', 'shield-lock', 'people', 'journal-text'],
                             menu_icon="app-indicator", 
                             default_index=0,
                             styles={
                                 "container": {"padding": "5!important", "background-color": "#fafafa"},
                                 "icon": {"color": "orange", "font-size": "25px"},
                                 "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                                 "nav-link-selected": {"background-color": "#02ab21"},
                             }
        )
    
    if choose == '종합':
        show_dashboard()
    elif choose == 'API 사용량':
        show_api_usage()
    elif choose == '서버 및 시스템':
        show_system_performance()
    elif choose == 'DB 관리':
        show_database_management()
    elif choose == '보안 현황':
        show_security_status()
    elif choose == '사용자 관리':
        show_user_management()
    elif choose == '로그 분석':
        show_log_analysis()

#####################################################################
# 제목 : 기본 대시보드
# 수정 날짜 : 2024-07-10
# 작성자 : 장지헌
# 수정자 : 장지헌
# 수정 내용 : 레이아웃 조정, 이미지 추가
#####################################################################
def show_dashboard():
    st.title("대시보드")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="활성 사용자 수", value="1,327", delta="32")
    with col2:
        st.metric(label="일일 로그인 수", value="2,071", delta=None)
    with col3:
        st.metric(label="서버 응답 시간", value="24 ms", delta="-3ms")
    with col4:
        st.metric(label="CPU 사용률", value="45%", delta="5%")
    
    st.subheader("서버 모니터링")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("CPU 사용률")
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 57,
            title = {'text': "CPU 사용률 (%)"},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "royalblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': "green"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        fig.update_layout(height=200, margin=dict(l=10, r=10, t=50, b=10), paper_bgcolor="rgba(0,0,0,0)", font_color="#FFFFFF")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("트래픽")
        st.subheader("CPU 사용률")
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 67,
            title = {'text': "CPU 사용률 (%)"},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "royalblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': "green"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        fig.update_layout(height=200, margin=dict(l=10, r=10, t=50, b=10), paper_bgcolor="rgba(0,0,0,0)", font_color="#FFFFFF")
        st.plotly_chart(fig, use_container_width=True)
        
    with col3:
        st.subheader("메모리 사용량")
        st.subheader("CPU 사용률")
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 50,
            title = {'text': "CPU 사용률 (%)"},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "royalblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': "green"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        fig.update_layout(height=200, margin=dict(l=10, r=10, t=50, b=10), paper_bgcolor="rgba(0,0,0,0)", font_color="#FFFFFF")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("API 사용량")
    df = pd.read_csv('datasets/api_usage.csv')
    df['date'] = pd.to_datetime(df['date'])
    
    fig = px.area(df, x="date", y="calls", color="api_name", title="API 사용량 추이")
    fig.update_layout(
        xaxis_title="날짜",
        yaxis_title="API 호출 횟수",
        legend_title="API 종류",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF"
    )
    st.plotly_chart(fig, use_container_width=True)

    
    col4, col5 = st.columns(2)
    with col4:
        st.subheader("DB")
        db_usage = 65
        st.write(f"총 용량 대비 사용 용량: {db_usage}%")
        st.progress(db_usage / 100)
        st.write("사용 347GB / 총 534GB")

        st.subheader("기능별 데이터베이스 사용률")
        db_usage_by_feature = {
            'AI 비서': 30,
            '교과서': 35,
            '수업 시간': 20,
            '학생 관리': 15
        }
        fig = px.pie(values=list(db_usage_by_feature.values()), names=list(db_usage_by_feature.keys()), title="기능별 데이터베이스 사용률")
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#FFFFFF"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col5:
        st.subheader("시스템 상태")
        
        # 시스템 상태
        system_status = "정상"
        if system_status == "정상":
            st.success(f"시스템 상태: {system_status}")
        else:
            st.error(f"시스템 상태: {system_status}")
        
        # 이미지 추가
        st.image("image\재혁쓰.jpg", width=200)
        
        # 추가 정보
        st.markdown("---")  # 구분선 추가
        st.write("**한국교육학술정보원**")
        st.write("전산실 팀장: 장재혁")

#####################################################################
# 제목 : 관리자 페이지
# 수정 날짜 : 2024-07-4
# 작성자 : 장지헌
# 수정자 : 장지헌
# 수정 내용 : API 대시보드 함수 완성
#####################################################################
def show_api_usage():
    st.title("API 사용량")
    
    # API 사용량 데이터 로드
    df = pd.read_csv('datasets/api_usage.csv')
    df['date'] = pd.to_datetime(df['date'])
    
    # 일별 API 사용량
    fig_daily = px.bar(df, x="api_name", y="calls", color="api_name", 
                       title="일별 API 호출 횟수", 
                       animation_frame=df['date'].dt.strftime('%Y-%m-%d'), 
                       range_y=[0,max(df['calls'])*1.1])
    fig_daily.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF"
    )
    st.plotly_chart(fig_daily, use_container_width=True)
    
    # 주간 API 사용량
    df_weekly = df.groupby(['api_name', pd.Grouper(key='date', freq='W-MON')])['calls'].sum().reset_index()
    fig_weekly = px.line(df_weekly, x="date", y="calls", color="api_name", title="주간 API 사용량")
    fig_weekly.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF"
    )
    st.plotly_chart(fig_weekly, use_container_width=True)
    
    # 월간 API 사용량
    df_monthly = df.groupby(['api_name', pd.Grouper(key='date', freq='MS')])['calls'].sum().reset_index()
    fig_monthly = px.line(df_monthly, x="date", y="calls", color="api_name", title="월간 API 사용량")
    fig_monthly.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF"
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

#####################################################################
# 제목 : 서버 퍼포먼스 대시보드
# 수정 날짜 : 2024-07-04
# 작성자 : 장지헌
# 수정자 : 장지헌
# 수정 내용 : 서버 퍼포먼스 대시보드 함수 완성
#####################################################################
def show_system_performance():
    st.title("서버 및 시스템")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 420,
            title = {'text': "서버 핑 (ms)"},
            gauge = {'axis': {'range': [None, 1000]},
                     'bar': {'color': "darkblue"},
                     'steps' : [
                         {'range': [0, 250], 'color': "green"},
                         {'range': [250, 500], 'color': "yellow"},
                         {'range': [500, 1000], 'color': "red"}],
                     'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 800}}))
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#FFFFFF"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.header('서버 핑')
        st.write("서버 핑은 서버의 응답 속도를 나타냅니다. 250ms 이하는 정상, 250-500ms는 주의, 500ms 이상은 위험 상태입니다.")
    
    with col2:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 65,
            title = {'text': "CPU 사용률 (%)"},
            gauge = {'axis': {'range': [None, 100]},
                     'bar': {'color': "darkblue"},
                     'steps' : [
                         {'range': [0, 50], 'color': "green"},
                         {'range': [50, 80], 'color': "yellow"},
                         {'range': [80, 100], 'color': "red"}],
                     'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}}))
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#FFFFFF"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.header('CPU 사용률')
        st.write("CPU 사용률은 서버의 처리 부하를 나타냅니다. 50% 이하는 정상, 50-80%는 주의, 80% 이상은 위험 상태입니다.")
    
    # 메모리 사용량 추가
    st.subheader("메모리 사용량")
    memory_usage = np.random.randint(40, 80)
    st.progress(memory_usage)
    st.write(f"현재 메모리 사용량: {memory_usage}%")

    # 네트워크 트래픽 추가
    st.subheader("네트워크 트래픽")
    network_in = np.random.randint(50, 200)
    network_out = np.random.randint(50, 200)
    st.metric(label="네트워크 입력", value=f"{network_in} Mbps")
    st.metric(label="네트워크 출력", value=f"{network_out} Mbps")

#####################################################################
# 제목 : DB 대시보드
# 수정 날짜 : 2024-07-04
# 작성자 : 장지헌
# 수정자 : 장지헌
# 수정 내용 : DB 대시보드 함수 완성
#####################################################################
def show_database_management():
    st.title("DB 관리")
    
    # DB 사용량 데이터 로드
    db_usage = pd.read_csv('datasets/db_usage.csv')
    db_usage['date'] = pd.to_datetime(db_usage['date'])
    
    st.subheader("DB 사용량")
    latest_usage = db_usage.iloc[-1]
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="총 용량", value=f"{latest_usage['total_capacity']} GB")
    with col2:
        usage_percentage = (latest_usage['used_capacity'] / latest_usage['total_capacity']) * 100
        st.metric(label="사용 중인 용량", value=f"{latest_usage['used_capacity']} GB", delta=f"{usage_percentage:.1f}%")
    
    # DB 사용량 추이 그래프
    fig = px.line(db_usage, x='date', y=['total_capacity', 'used_capacity'], title="DB 용량 사용 추이")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("최근 쿼리 성능")
    query_performance = pd.read_csv('datasets/query_performance.csv')
    query_performance['timestamp'] = pd.to_datetime(query_performance['timestamp'])
    st.dataframe(query_performance, height=300, width=1100)
    
    # 쿼리 유형별 평균 실행 시간
    avg_query_time = query_performance.groupby('query')['execution_time'].mean().reset_index()
    fig = px.bar(avg_query_time, x='query', y='execution_time', title="쿼리 유형별 평균 실행 시간")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF"
    )
    st.plotly_chart(fig, use_container_width=True)

#####################################################################
# 제목 : 보안현황 대시보드
# 수정 날짜 : 2024-07-05
# 작성자 : 장지헌
# 수정자 : 장지헌
# 수정 내용 : 보안현황 대시보드 함수 완성
#####################################################################
def show_security_status():
    st.title("보안 현황")
    
    # 로그인 시도 데이터 로드
    login_attempts = pd.read_csv('datasets/login_attempts.csv')
    login_attempts['timestamp'] = pd.to_datetime(login_attempts['timestamp'])
    
    st.subheader("최근 로그인 시도")
    st.dataframe(login_attempts, height=400, width=1100)  # 높이를 400픽셀로 설정
    
    # 로그인 성공/실패 비율
    login_status = login_attempts['status'].value_counts()
    fig = px.pie(values=login_status.values, names=login_status.index, title="로그인 성공/실패 비율")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 시간대별 로그인 시도 횟수
    login_attempts['hour'] = login_attempts['timestamp'].dt.hour
    hourly_attempts = login_attempts.groupby('hour').size().reset_index(name='count')
    fig = px.line(hourly_attempts, x='hour', y='count', title="시간대별 로그인 시도 횟수")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("SSL 인증서 상태")
    st.info("SSL 인증서가 유효합니다. 만료일: 2025-07-01")

#####################################################################
# 제목 : 사용자관리 대시보드
# 수정 날짜 : 2024-07-05
# 작성자 : 장지헌
# 수정자 : 장지헌
# 수정 내용 : 사용자관리 대시보드 함수 완성
#####################################################################
def show_user_management():
    st.title("사용자 관리")
    
    user_data = pd.read_csv('datasets/users.csv')
    user_data['last_login'] = pd.to_datetime(user_data['last_login'])
    st.table(user_data)
    
    st.subheader("새 사용자 추가")
    col1, col2 = st.columns(2)
    with col1:
        new_name = st.text_input("이름")
    with col2:
        new_role = st.selectbox("역할", ["학생", "교사", "관리자"])
    if st.button("사용자 추가"):
        st.success("새 사용자가 추가되었습니다.")

#####################################################################
# 제목 : 로그 대시보드
# 수정 날짜 : 2024-07-05
# 작성자 : 장지헌
# 수정자 : 장지헌
# 수정 내용 : 로그 대시보드 함수 완성
#####################################################################
def show_log_analysis():
    st.title("로그 분석")
    
    log_data = pd.read_csv('datasets/logs.csv')
    log_data['timestamp'] = pd.to_datetime(log_data['timestamp'])
    
    # 스크롤 가능한 데이터프레임으로 표시
    st.dataframe(log_data, height=400, width=1100)  # 높이를 400픽셀로 설정
    
    st.subheader("로그 검색")
    search_term = st.text_input("검색어 입력")
    if st.button("검색"):
        search_results = log_data[log_data.apply(lambda row: search_term.lower() in row.astype(str).str.lower().to_string(), axis=1)]
        st.write(f"'{search_term}'에 대한 검색 결과입니다.")
        
        # 검색 결과도 스크롤 가능한 데이터프레임으로 표시
        if not search_results.empty:
            st.dataframe(search_results, height=300)  # 높이를 300픽셀로 설정
        else:
            st.write("검색 결과가 없습니다.")

if __name__ == "__main__":
    main("관리자")
