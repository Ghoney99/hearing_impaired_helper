import requests
from urllib.parse import urlencode
import xml.etree.ElementTree as ET

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

# 입력
text = '감자'

# 출력
results = get_video(text)
if results:
    for result in results:
        title = result['title']
        sub_description = result['sub_description']
        description = result['description']
        image_object = result['image_object']
        
        print(f"Title: {title}")
        print(f"Sub Description: {sub_description}")
        print(f"Description: {description}")
        print(f"Image Object: {image_object}")
        print()
