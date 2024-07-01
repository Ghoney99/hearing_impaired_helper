import streamlit as st

# 수어 단어장 라이브러리
import requests
from urllib.parse import urlencode
import xml.etree.ElementTree as ET

#####################################################################
# 제목 : 수어 단어장
# 수정 날짜 : 2024-06-28
# 작성자 : 장지헌
# 수정자 : 장재혁
# 수정 내용 : 수어 단어장 파일 생성
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
