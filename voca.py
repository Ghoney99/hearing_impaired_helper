import streamlit as st

# 수어 단어장 라이브러리
import requests
from urllib.parse import urlencode
import xml.etree.ElementTree as ET
import speech_recognition as sr

#####################################################################
# 제목 : 수어 단어장
# 수정 날짜 : 2024-07-16
# 작성자 : 장지헌
# 수정자 : 장재혁
# 수정 내용 : 구조 오른쪽으로 옮김
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

def main():
    con1, con2 = st.columns([2,1])
    with con1:
        pass
    
    with con2:
        st.title("수어 사전")
        
        text = st.text_input("단어를 입력하세요!")
        results = get_video(text)
        
        if results:
            for i, result in enumerate(results):
                full_title = result['title']
                words = full_title.split(',')
                main_title = words[0].strip()  # 첫 번째 단어를 메인 타이틀로 사용
                sub_description = result['sub_description']
                description = result['description']
                image_object = result['image_object']
                
                # 각 결과에 대한 고유한 키 생성
                key_base = f"{i}_{main_title}"
                
                # session_state를 사용하여 각 버튼의 상태 초기화
                if f"대응표현_{key_base}" not in st.session_state:
                    st.session_state[f"대응표현_{key_base}"] = False
                if f"추천어휘_{key_base}" not in st.session_state:
                    st.session_state[f"추천어휘_{key_base}"] = False
                if f"필수어휘_{key_base}" not in st.session_state:
                    st.session_state[f"필수어휘_{key_base}"] = False
                
                # 카드 형태로 UI 구성하기
                with st.expander(main_title):
                    st.image(image_object)  # 이미지를 표시
                    st.markdown(f"설명 : {description}")
                    st.markdown(f"[{main_title}]({sub_description})")
                    
                    # 버튼들 생성
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("대응표현", key=f"대응표현_btn_{key_base}"):
                            st.session_state[f"대응표현_{key_base}"] = not st.session_state[f"대응표현_{key_base}"]
                    
                    with col2:
                        if st.button("추천어휘", key=f"추천어휘_btn_{key_base}"):
                            st.session_state[f"추천어휘_{key_base}"] = not st.session_state[f"추천어휘_{key_base}"]
                    
                    with col3:
                        if st.button("필수어휘", key=f"필수어휘_btn_{key_base}"):
                            st.session_state[f"필수어휘_{key_base}"] = not st.session_state[f"필수어휘_{key_base}"]
                    
                    # 각 버튼의 내용 표시
                    if st.session_state[f"대응표현_{key_base}"] and len(words) > 1:
                        st.write("대응표현:")
                        for word in words[1:]:
                            st.write(f"- {word.strip()}")
                    
                    if st.session_state[f"추천어휘_{key_base}"]:
                        st.write("추천어휘: 미구현")
                    
                    if st.session_state[f"필수어휘_{key_base}"]:
                        st.write("필수어휘: 미구현")
                        
#####################################################################
#####################################################################
