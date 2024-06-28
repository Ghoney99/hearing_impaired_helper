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
from openai import OpenAI
import requests
from urllib.parse import urlencode
import xml.etree.ElementTree as ET


# 터미널 창에 입력해서 실행
# streamlit run test.py

st.set_page_config(layout="wide")

#####################################################################
# 제목 : 함수 모음
# 수정 날짜 : 2024-06-28
# 작성자 : 장지헌
# 수정자 : 장지헌
# 수정 내용 : 
#####################################################################
def parse_response(response_text):
    root = ET.fromstring(response_text)
    
    items = root.findall('.//item')
    
    results = []
    for item in items:
        title = item.find('title').text
        sub_description = item.find('subDescription').text if item.find('subDescription') is not None else ''
        description = item.find('description').text if item.find('description') is not None else ''
        image_object = item.find('imageObject').text if item.find('imageObject') is not None else ''
        
        results.append({
            'title': title,
            'sub_description': sub_description,
            'description': description,
            'image_object': image_object
        })
    
    return results

def get_video(keyword):
    base_url = "http://api.kcisa.kr/API_CNV_054/request"
    params = {
        "serviceKey": "d8fb6910-dfc1-47ca-bb0a-16924ea0e629",
        "numOfRows": "5",
        "pageNo": "1",
        "keyword": keyword
    }
    
    url = f"{base_url}?{urlencode(params)}"
    
    headers = {
        "Content-type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    print(f"Response code: {response.status_code}")
    
    if 200 <= response.status_code <= 300:
        return parse_response(response.text)
    else:
        print("Error:", response.text)
        return None
#####################################################################

#####################################################################
# 제목 : Title
# 수정 날짜 : 2024-06-28
# 작성자 : 장재혁
# 수정자 : 장지헌
# 수정 내용 : 수어 단어장 추가
#####################################################################
with st.sidebar:
    choose = option_menu("AI 디지털 교과서", ["STT", "수어 도우미", "AI Tutor", '수어 단어장'],
                         icons=['house', 'camera fill', 'kanban'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )
#####################################################################



#####################################################################
# 제목 : Ai Tutor
# 수정 날짜 : 2024-06-28
# 작성자 : 장재혁
# 수정자 : 장지헌
# 수정 내용 : 
#####################################################################
if choose == "AI Tutor":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.image("20240627_214541.png", caption="국어", use_column_width=True)

    with col2:
        st.title("AI 튜터")

        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo"

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("What is up?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
#####################################################################


#####################################################################
# 제목 : STT
# 수정 날짜 : 2024-06-28
# 작성자 : 장재혁
# 수정자 : 장재혁
# 수정 내용 : 
#####################################################################
elif choose == "STT":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.image("20240627_214541.png", caption="국어", use_column_width=True)

    with col2:
        st.title("Speech-to-Text (STT) App")
        st.write("STT 관련 콘텐츠")
#####################################################################


#####################################################################
# 제목 : 수어 도우미
# 수정 날짜 : 2024-06-28
# 작성자 : 장지헌
# 수정자 : 장지헌
# 수정 내용 : 
#####################################################################
elif choose == "수어 도우미":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.image("20240627_214541.png", caption="국어", use_column_width=True)

    with col2:
        st.title("수어 도우미 (Sign Language Helper) App")
        st.write("수어 도우미 관련 콘텐츠")
#####################################################################


#####################################################################
# 제목 : 수어 단어장
# 수정 날짜 : 2024-06-28
# 작성자 : 장지헌
# 수정자 : 장지헌
# 수정 내용 : 
#####################################################################
elif choose == "수어 단어장":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.image("20240627_214541.png", caption="국어", use_column_width=True)

    with col2:
        st.title("수어 단어장 (Sign Language Helper) App")
        text = st.text_input("단어를 입력하세요!")
        results = get_video(text)
        
        if results:
            for result in results:
                title = result['title']
                sub_description = result['sub_description']
                description = result['description']
                image_object = result['image_object']
                
            # 카드 형태로 UI 구성하기
            with st.expander(title):
                st.image(image_object)  # 이미지를 표시하려면 이미지 경로나 이미지 자체를 전달합니다
                st.markdown(f"설명 : {description}")
                st.markdown(f"[{title}]({sub_description})")
#####################################################################

