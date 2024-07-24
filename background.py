import streamlit as st

# #####################################################################
# # 제목 : 배경
# # 수정 날짜 : 2024-07-22
# # 작성자 : 장재혁
# # 수정자 : 장지헌
# # 수정 내용 : admin페이지 함수 생성
# #####################################################################

# 로그인페이지
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://i.imgur.com/VYuh8hu.png");
             background-attachment: fixed;
             background-size: auto
             
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# 학생 대시보드
def add_bg_from_url2():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://i.imgur.com/rYK5vKf.png?1");
             background-attachment: fixed;
             background-size: auto
             
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# 교과서 목록    
def add_bg_from_url3():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://i.imgur.com/9uz3b8L.png");
             background-attachment: fixed;
             background-size: auto;
             
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
    
# 국어 교과서 페이지
def add_bg_from_url4():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-attachment: fixed;
             background-size: auto
             
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# 빈페이지
def add_bg_from_url5():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("");
             background-attachment: fixed;
             background-size: auto
             
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
    
# 수어단어장
def add_bg_from_url6():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://i.imgur.com/DWtt6iH.png");
             background-attachment: fixed;
             background-size: auto
             
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# admin페이지
def add_bg_from_url_admin():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://e1.pxfuel.com/desktop-wallpaper/225/563/desktop-wallpaper-9-white-backgrounds-iphone-white.jpg");
             background-attachment: fixed;
             background-size: auto
             
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
