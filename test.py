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

import sys
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import Sign_Language_Translation.modules.holistic_module as hm
from tensorflow.keras.models import load_model
import math
from Sign_Language_Translation.modules.utils import Vector_Normalization
from PIL import ImageFont, ImageDraw, Image
from Sign_Language_Translation.unicode import join_jamos

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

# 수어 단어장 -> API 불러오기
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

# 수어 단어장 -> API 처리 
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
    
# 수어 인식 -> 자모음 병합
def jamo_trans(jamo):

    chars = list(set(jamo))
    char_to_ix = { ch:i for i,ch in enumerate(chars) }
    ix_to_char = { i:ch for i,ch in enumerate(chars) }

    jamo_numbers = [char_to_ix[x] for x in jamo]

    restored_jamo = ''.join([ix_to_char[x] for x in jamo_numbers])
    restored_text = join_jamos(restored_jamo)
    return restored_text

# 수어 인식 -> 리스트 추가 함수
def add_unique_element(lst, element):
    if not lst or lst[-1] != element:
        lst.append(element)
    return lst
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
        
        result_word = ''
        
        if st.button('데이터 보기'):
            fontpath = "fonts/HMKMMAG.TTF"
            font = ImageFont.truetype(fontpath, 40)

            actions = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ',
                        'ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ',
                        'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ', 'ㅢ', 'ㅚ', 'ㅟ']
            seq_length = 10

            # MediaPipe holistic model
            detector = hm.HolisticDetector(min_detection_confidence=0.3)

            # Load TFLite model and allocate tensors.
            interpreter = tf.lite.Interpreter(model_path="models/multi_hand_gesture_classifier.tflite")
            interpreter.allocate_tensors()

            # Get input and output tensors.
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()

            cap = cv2.VideoCapture(0)

            seq = []
            action_seq = []
            last_action = None

            # zamo_list=[]
            textArr = list()
            while cap.isOpened():
                ret, img = cap.read()
                if not ret:
                    break

                img = detector.findHolistic(img, draw=True)
                # _, left_hand_lmList = detector.findLefthandLandmark(img)
                _, right_hand_lmList = detector.findRighthandLandmark(img)

                # if left_hand_lmList is not None and right_hand_lmList is not None:
                if right_hand_lmList is not None:

                    joint = np.zeros((42, 2))
                    # 왼손 랜드마크 리스트
                    # for j, lm in enumerate(left_hand_lmList.landmark):
                        # joint[j] = [lm.x, lm.y]
                    
                    # 오른손 랜드마크 리스트
                    for j, lm in enumerate(right_hand_lmList.landmark):
                        # joint[j+21] = [lm.x, lm.y]
                        joint[j] = [lm.x, lm.y]

                    # 좌표 정규화
                    # full_scale = Coordinate_Normalization(joint)

                    # 벡터 정규화
                    vector, angle_label = Vector_Normalization(joint)

                    # 위치 종속성을 가지는 데이터 저장
                    # d = np.concatenate([joint.flatten(), angle_label])
                
                    # 벡터 정규화를 활용한 위치 종속성 제거
                    d = np.concatenate([vector.flatten(), angle_label.flatten()])

                    # 정규화 좌표를 활용한 위치 종속성 제거 
                    # d = np.concatenate([full_scale, angle_label.flatten()])
                    

                    seq.append(d)

                    if len(seq) < seq_length:
                        continue

                    # Test model on random input data.
                    # input_shape = input_details[0]['shape']
                    # input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
                    
                    # 시퀀스 데이터와 넘파이화
                    input_data = np.expand_dims(np.array(seq[-seq_length:], dtype=np.float32), axis=0)
                    input_data = np.array(input_data, dtype=np.float32)

                    # tflite 모델을 활용한 예측
                    interpreter.set_tensor(input_details[0]['index'], input_data)
                    interpreter.invoke()

                    y_pred = interpreter.get_tensor(output_details[0]['index'])
                    i_pred = int(np.argmax(y_pred[0]))
                    conf = y_pred[0][i_pred]

                    if conf < 0.9:
                        continue

                    action = actions[i_pred]
                    action_seq.append(action)

                    if len(action_seq) < 3:
                        continue

                    this_action = '?'
                    if action_seq[-1] == action_seq[-2] == action_seq[-3]:
                        this_action = action

                        if last_action != this_action:
                            last_action = this_action
                    '''
                    # 기록된 한글 파악
                    if zamo_list[-1] != this_action: # 만약 전에 기록된 글자와 이번 글자가 다르다면
                        zamo_list.append(this_action)
                    
                    zamo_str = ''.join(zamo_list) # 리스트에 있는 단어 합침
                    unitl_action = join_jamos(zamo_str) # 합친 단어 한글로 만들기
                    '''
                    
                    # 한글 폰트 출력    
                    img_pil = Image.fromarray(img)
                    draw = ImageDraw.Draw(img_pil)
                    '''
                    draw.text((int(right_hand_lmList.landmark[0].x * img.shape[1]), int(right_hand_lmList.landmark[0].y * img.shape[0] + 20)),
                            f'{this_action.upper()}', 
                            font=font, 
                            fill=(255, 255, 255))
                    '''
                    draw.text((10, 30), f'{action.upper()}', font=font, fill=(255, 255, 255))
                    draw.text((10, 70), f'{result_word}', font=font, fill=(255, 255, 255))
                    img = np.array(img_pil)
                    
                    #분류된 글자 출력 : this_action
                    if this_action != '?':
                        add_unique_element(textArr, this_action)
                    result_word = jamo_trans(textArr)
                    print(result_word)
                    
                    # cv2.putText(img, f'{this_action.upper()}', org=(int(right_hand_lmList.landmark[0].x * img.shape[1]), int(right_hand_lmList.landmark[0].y * img.shape[0] + 20)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)


                cv2.imshow('img', img)
                if cv2.waitKey(70) & 0xFF == 27:
                    break
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

