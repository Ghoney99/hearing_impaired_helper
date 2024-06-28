import sys
# sys.path.append('pingpong')
# from pingpong.pingpongthread import PingPongThread
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import modules.holistic_module as hm
from tensorflow.keras.models import load_model
import math
from modules.utils import Vector_Normalization
from PIL import ImageFont, ImageDraw, Image
# from hangul_utils import join_jamos
from unicode import join_jamos  #노트북 환경이슈로 unicode.py에서 함수 import

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
# 종료버튼 좌표
button_coords = (50, 50, 200, 100)

def draw_button(img, coords, text, color=(0, 0, 255)):
    x1, y1, x2, y2 = coords
    cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, text, (x1 + 20, y1 + 35), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

def check_button_click(event, x, y, flags, param):
    global running
    if event == cv2.EVENT_LBUTTONDOWN:
        if button_coords[0] <= x <= button_coords[2] and button_coords[1] <= y <= button_coords[3]:
            running = False

running = True
cv2.namedWindow('img')
cv2.setMouseCallback('img', check_button_click)

while cap.isOpened() and running:
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
        
        # 한글 폰트 출력    
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        draw.text((10, 30), f'{action.upper()}', font=font, fill=(255, 255, 255))

        img = np.array(img_pil)
        
        #분류된 글자 출력 : this_action
        if this_action != '?':
            add_unique_element(textArr, this_action)
        result_word = jamo_trans(textArr)
        print(result_word)
        
    draw_button(img, button_coords, "EXIT")
    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
