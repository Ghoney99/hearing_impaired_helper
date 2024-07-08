import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# st.set_page_config(layout="wide", page_title="관리자 대시보드", page_icon="🔐")

# CSS를 사용하여 다크모드 스타일 적용
st.markdown("""
<style>
    .reportview-container {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .sidebar .sidebar-content {
        background-color: #2E2E2E;
    }
    .Widget>label {
        color: #FFFFFF;
    }
    .stPlotlyChart {
        background-color: #2E2E2E;
    }
</style>
""", unsafe_allow_html=True)

def main(admin_name):
    st.sidebar.title(f"환영합니다, {admin_name}")
    
    menu = st.sidebar.selectbox(
        "메뉴 선택",
        ["기본 대시보드", "API 사용량", "시스템 성능", "데이터베이스 관리", "보안 현황", "사용자 관리", "로그 분석"]
    )
    
    if menu == "기본 대시보드":
        show_dashboard()
    elif menu == "API 사용량":
        show_api_usage()
    elif menu == "시스템 성능":
        show_system_performance()
    elif menu == "데이터베이스 관리":
        show_database_management()
    elif menu == "보안 현황":
        show_security_status()
    elif menu == "사용자 관리":
        show_user_management()
    elif menu == "로그 분석":
        show_log_analysis()

def show_dashboard():
    st.title("관리자 대시보드")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="활성 사용자 수", value="1,234", delta="32")
    with col2:
        st.metric(label="일일 로그인 수", value="5,678", delta="-12") 
    with col3:
        st.metric(label="서버 응답 시간", value="24 ms", delta="-3 ms")
    with col4:
        st.metric(label="CPU 사용률", value="45%", delta="5%")
    
    # 일일 로그인 데이터 로드
    df = pd.read_csv('datasets/daily_logins.csv')
    df['date'] = pd.to_datetime(df['date'])
    
    # 일일 로그인 추이
    fig_daily = px.line(df, x="date", y="logins", title="일일 로그인 추이")
    fig_daily.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF"
    )
    st.plotly_chart(fig_daily, use_container_width=True)
    
    # 주간 로그인 추이
    df_weekly = df.resample('W', on='date').sum().reset_index()
    fig_weekly = px.line(df_weekly, x="date", y="logins", title="주간 로그인 추이")
    fig_weekly.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF"
    )
    st.plotly_chart(fig_weekly, use_container_width=True)
    
    # 월간 로그인 추이
    df_monthly = df.resample('M', on='date').sum().reset_index()
    fig_monthly = px.line(df_monthly, x="date", y="logins", title="월간 로그인 추이")
    fig_monthly.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF"
    )
    st.plotly_chart(fig_monthly, use_container_width=True)
    
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

def show_system_performance():
    st.title("시스템 성능")
    
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

def show_database_management():
    st.title("데이터베이스 관리")
    
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
