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
import matplotlib.pyplot as plt
from openai import OpenAI

# 수어 단어장 라이브러리
import requests
from urllib.parse import urlencode
import xml.etree.ElementTree as ET

# 수어 인식 모델 라이브러리
from Sign_Language_Translation.modules.utils import Vector_Normalization
from PIL import ImageFont, ImageDraw, Image
from Sign_Language_Translation.unicode import join_jamos
import tensorflow as tf
import Sign_Language_Translation.modules.holistic_module as hm
from tensorflow.keras.models import load_model
import cv2s
import mediapipe as mp
import numpy as np

# STT 라이브러리
import speech_recognition as sr # 라이브러리 설치


# 실행 코드
# streamlit run test.py


# 글꼴 설정
plt.rcParams['font.family'] ='Malgun Gothic'

#####################################################################
# 제목 : 함수 모음
# 수정 날짜 : 2024-07-01
# 작성자 : 장지헌
# 수정자 : 장지헌
# 수정 내용 : stt 함수 추가
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

# 수어 인식 -> result 값
result_word = ''

# STT 함수
def speech_to_text(recognizer):
    with sr.Microphone() as source:
        st.write("[자막]")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language='ko-KR')
        st.write(f"{text}") # 결과값 출력
        return text
    except sr.UnknownValueError:
        st.write("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        st.write(f"음성 인식 서비스에 접근할 수 없습니다: {e}")
        
#####################################################################



#####################################################################
# 제목 : 사이드바
# 수정 날짜 : 2024-06-28
# 작성자 : 장재혁
# 수정자 : 장지헌
# 수정 내용 : 수어 단어장 추가
#####################################################################
st.set_page_config(layout="wide")

with st.sidebar:
    choose = option_menu("AI 디지털 교과서", ["STT", "수어 도우미", "AI Tutor",'성적 확인', '수어 단어장'],
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
# 제목 : Ai 튜터
# 수정 날짜 : 2024-06-28
# 작성자 : 장재혁
# 수정자 : 장재혁
# 수정 내용 : 파인튜닝
#####################################################################
if choose == "AI Tutor":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.image("20240627_214541.png", caption="국어", use_column_width=True)
        
        
    with col2:
        st.title("AI 튜터")

        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "ft:gpt-3.5-turbo-0125:personal::9evZE1BR"

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
# 수정 날짜 : 2024-07-01
# 작성자 : 장지헌
# 수정자 : 장지헌
# 수정 내용 : stt 기능 러프하게 추가
#####################################################################
elif choose == "STT":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.image("20240627_214541.png", caption="국어", use_column_width=True)

    with col2:
        st.title("Speech-to-Text (STT) App")
        st.write("STT 관련 콘텐츠")
        # Recognizer 객체 생성
        recognizer = sr.Recognizer()

        # Streamlit 애플리케이션 정의
        st.title("마이크로부터 텍스트로 변환하기")

        st.write("마이크를 통해 음성을 입력하고 '인식' 버튼을 클릭하세요.")

        if st.button("인식"):
            result = speech_to_text(recognizer)
#####################################################################


#####################################################################
# 제목 : 수어 도우미
# 수정 날짜 : 2024-07-01
# 작성자 : 장지헌
# 수정자 : 장지헌
# 수정 내용 : 수어 인식 모델 새창을 띄워서 인식
#####################################################################
elif choose == "수어 도우미":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.image("20240627_214541.png", caption="국어", use_column_width=True)

    with col2:
        st.title("수어 도우미 (Sign Language Helper) App")
        st.write("수어 도우미 관련 콘텐츠")
        
        fontpath = "fonts/HMKMMAG.TTF"
        font = ImageFont.truetype(fontpath, 40)
        textArr = list()

        # TFLite 모델 로드 및 초기화
        interpreter = tf.lite.Interpreter(model_path="models/multi_hand_gesture_classifier.tflite")
        interpreter.allocate_tensors()

        # 입력 및 출력 텐서 가져오기
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # 스트림릿 앱 레이아웃 및 버튼 생성
        st.title('Gesture Recognition with Streamlit')

        # 카메라 캡처 객체와 관련 변수 초기화
        cap = None
        seq = []
        action_seq = []
        last_action = None
        detector = hm.HolisticDetector(min_detection_confidence=0.3)

        # 'Run Gesture Recognition' 버튼 클릭 시 동작
        if st.button('Run Gesture Recognition'):
            result_word = ''

            # 카메라 캡처 시작
            cap = cv2.VideoCapture(0)

            while cap and cap.isOpened():
                ret, img = cap.read()
                if not ret:
                    break

                img = detector.findHolistic(img, draw=True)
                _, right_hand_lmList = detector.findRighthandLandmark(img)

                if right_hand_lmList is not None:
                    joint = np.zeros((42, 2))

                    for j, lm in enumerate(right_hand_lmList.landmark):
                        joint[j] = [lm.x, lm.y]

                    vector, angle_label = Vector_Normalization(joint)
                    d = np.concatenate([vector.flatten(), angle_label.flatten()])

                    seq.append(d)

                    if len(seq) < 10:
                        continue

                    input_data = np.expand_dims(np.array(seq[-10:], dtype=np.float32), axis=0)
                    input_data = np.array(input_data, dtype=np.float32)

                    interpreter.set_tensor(input_details[0]['index'], input_data)
                    interpreter.invoke()

                    y_pred = interpreter.get_tensor(output_details[0]['index'])
                    i_pred = int(np.argmax(y_pred[0]))
                    conf = y_pred[0][i_pred]

                    if conf < 0.9:
                        continue

                    actions = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ',
                            'ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ',
                            'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ', 'ㅢ', 'ㅚ', 'ㅟ']
                    action = actions[i_pred]
                    action_seq.append(action)

                    if len(action_seq) < 3:
                        continue

                    this_action = '?'
                    if action_seq[-1] == action_seq[-2] == action_seq[-3]:
                        this_action = action

                        if last_action != this_action:
                            last_action = this_action

                    img_pil = Image.fromarray(img)
                    draw = ImageDraw.Draw(img_pil)
                    draw.text((10, 30), f'{action.upper()}', font=font, fill=(255, 255, 255))
                    draw.text((10, 70), f'{result_word}', font=font, fill=(255, 255, 255))
                    img = np.array(img_pil)

                    if this_action != '?':
                        add_unique_element(textArr, this_action)
                    result_word = jamo_trans(textArr)

                cv2.imshow('img', img)
                key = cv2.waitKey(70) & 0xFF
                if key == 27:  # 'esc' 키를 누르면
                    break

        # 카메라와 윈도우를 정리
        if cap:
            cap.release()
        cv2.destroyAllWindows()


#####################################################################




#####################################################################
# 제목 : 성적확인
# 수정 날짜 : 2024-06-28
# 작성자 : 장재혁
# 수정자 : 장재혁
# 수정 내용 : 성적확인 차트
#####################################################################
elif choose == "성적 확인":
    # 데이터셋 로드
    df = pd.read_csv('student_scores_korean_subjects.csv')

    # Ensure relevant columns are numeric
    for col in ['국어_중간고사', '국어_기말고사', '수학_중간고사', '수학_기말고사', '영어_중간고사', '영어_기말고사', '과학_중간고사', '과학_기말고사']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 학생 이름과 ID를 매핑
    student_name_to_id = {row['이름']: row['학생ID'] for _, row in df.iterrows()}

    def compare_student_with_average(df, student_id):
        student_data = df[df['학생ID'] == student_id]

        df['전체_평균_국어'] = df[['국어_중간고사', '국어_기말고사']].mean(axis=1)
        df['전체_평균_수학'] = df[['수학_중간고사', '수학_기말고사']].mean(axis=1)
        df['전체_평균_영어'] = df[['영어_중간고사', '영어_기말고사']].mean(axis=1)
        df['전체_평균_과학'] = df[['과학_중간고사', '과학_기말고사']].mean(axis=1)

        semester_avg = df.groupby('학기').mean(numeric_only=True).reset_index()

        student_data['학생_평균_국어'] = student_data[['국어_중간고사', '국어_기말고사']].mean(axis=1)
        student_data['학생_평균_수학'] = student_data[['수학_중간고사', '수학_기말고사']].mean(axis=1)
        student_data['학생_평균_영어'] = student_data[['영어_중간고사', '영어_기말고사']].mean(axis=1)
        student_data['학생_평균_과학'] = student_data[['과학_중간고사', '과학_기말고사']].mean(axis=1)

        student_avg = student_data.groupby('학기').mean(numeric_only=True).reset_index()

        fig, axs = plt.subplots(2, 2, figsize=(14, 10))
        subjects = ['국어', '수학', '영어', '과학']
        for i, subject in enumerate(subjects):
            ax = axs[i // 2, i % 2]
            ax.plot(semester_avg['학기'], semester_avg[f'전체_평균_{subject}'], label='전체 평균', marker='o')
            ax.plot(student_avg['학기'], student_avg[f'학생_평균_{subject}'], label='학생 평균', marker='o')
            ax.set_title(f'{subject} 성적 비교')
            ax.set_xlabel('학기')
            ax.set_ylabel('평균 성적')
            ax.legend()

        plt.tight_layout()
        st.pyplot(fig)

    # 사용자에게 이름을 입력받음
    student_name = st.text_input('학생 이름을 입력하세요:')
    if student_name:
        if student_name in student_name_to_id:
            student_id = student_name_to_id[student_name]
            compare_student_with_average(df, student_id)
        else:
            st.write("해당 이름의 학생을 찾을 수 없습니다.")
#####################################################################


      
            
#####################################################################
# 제목 : 수어 단어장
# 수정 날짜 : 2024-06-28
# 작성자 : 장지헌
# 수정자 : 장지헌
# 수정 내용 : 수어 단어장 추가
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
