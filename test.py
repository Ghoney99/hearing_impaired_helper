import requests

# 카카오 API 키
api_key = 'YOUR_KAKAO_API_KEY'

def get_related_words(query):
    # API 요청 URL
    url = 'https://dapi.kakao.com/v2/search/web'

    # 요청 헤더
    headers = {
        'Authorization': f'KakaoAK {api_key}'
    }

    # 요청 파라미터
    params = {
        'query': query
    }

    # API 요청 보내기
    response = requests.get(url, headers=headers, params=params)

    # 응답 확인
    if response.status_code == 200:
        data = response.json()
        # 검색 결과에서 연관 단어 추출 (여기서는 임의로 3개의 연관 단어를 출력하도록 함)
        documents = data.get('documents', [])
        related_words = [doc['title'] for doc in documents[:3]]
        return related_words
    else:
        print('Error:', response.status_code, response.text)
        return []

# 테스트
query = '배고파에 관련된 연관단어를 출력해줘'
related_words = get_related_words(query)
print(f'Query: {query}')
print('Related Words:', related_words)
