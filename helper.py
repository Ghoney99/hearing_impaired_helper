import streamlit as st

# 수어 인식 모델 라이브러리
from modules.utils import Vector_Normalization
from PIL import ImageFont, ImageDraw, Image
from modules.unicode import join_jamos
import tensorflow as tf
import modules.holistic_module as hm
import cv2
import mediapipe as mp
import numpy as np

#####################################################################
# 제목 : 수어 번역
# 수정 날짜 : 2024-07-16
# 작성자 : 장지헌
# 수정자 : 장재혁
# 수정 내용 : 타이틀메세지 빼고 버튼텍스트 변경
#####################################################################


# 자모음을 병합하는 함수
# 매개변수: jamo (str): 자모음 문자열
# 반환값: str: 병합된 문자열
def jamo_trans(jamo):

    chars = list(set(jamo))
    char_to_ix = { ch:i for i,ch in enumerate(chars) }
    ix_to_char = { i:ch for i,ch in enumerate(chars) }

    jamo_numbers = [char_to_ix[x] for x in jamo]

    restored_jamo = ''.join([ix_to_char[x] for x in jamo_numbers])
    restored_text = join_jamos(restored_jamo)
    return restored_text


# 리스트에 고유한 요소를 추가하는 함수
# 매개변수: lst (list): 대상 리스트, element: 추가할 요소
# 반환값: list: 업데이트된 리스트
def add_unique_element(lst, element):
    if not lst or lst[-1] != element:
        lst.append(element)
    return lst

# 수어 인식 -> result 값
result_word = ''

def main():
    
    fontpath = "fonts/HMKMMAG.TTF"
    font = ImageFont.truetype(fontpath, 40)
    textArr = list()

    # TFLite 모델 로드 및 초기화
    interpreter = tf.lite.Interpreter(model_path="models/multi_hand_gesture_classifier.tflite")
    interpreter.allocate_tensors()

    # 입력 및 출력 텐서 가져오기
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # 카메라 캡처 객체와 관련 변수 초기화
    cap = None
    seq = []
    action_seq = []
    last_action = None
    detector = hm.HolisticDetector(min_detection_confidence=0.3)

    # 'Run Gesture Recognition' 버튼 클릭 시 동작
    empty, con1, = st.columns([1,1])
    with empty:
        pass
    with con1:
        if st.button('수어 번역'):
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
                    # st.subheader(result_word)
                    break

    # 카메라와 윈도우를 정리
    if cap:
        cap.release()
    cv2.destroyAllWindows()