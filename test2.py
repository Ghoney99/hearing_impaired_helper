from Sign_Language_Translation.modules.utils import Vector_Normalization
from PIL import ImageFont, ImageDraw, Image # 라이브러리 설치
from Sign_Language_Translation.unicode import join_jamos
import tensorflow as tf
import Sign_Language_Translation.modules.holistic_module as hm
from tensorflow.keras.models import load_model # 라이브러리 설치
import cv2 # 라이브러리 설치
import mediapipe as mp # 라이브러리 설치
import numpy as np
import streamlit as st

# 자모음 병합
def jamo_trans(jamo):

    chars = list(set(jamo))
    char_to_ix = { ch:i for i,ch in enumerate(chars) }
    ix_to_char = { i:ch for i,ch in enumerate(chars) }

    jamo_numbers = [char_to_ix[x] for x in jamo]

    restored_jamo = ''.join([ix_to_char[x] for x in jamo_numbers])
    restored_text = join_jamos(restored_jamo)
    return restored_text

# 리스트 추가 함수
def add_unique_element(lst, element):
    if not lst or lst[-1] != element:
        lst.append(element)
    return lst

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

if st.button('Run Gesture Recognition'):
    result_word = ''

    # 캡처 및 처리 코드
    cap = cv2.VideoCapture(0)

    seq = []
    action_seq = []
    last_action = None

    detector = hm.HolisticDetector(min_detection_confidence=0.3)

    while cap.isOpened():
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
        if cv2.waitKey(70) & 0xFF == 27:
            break

