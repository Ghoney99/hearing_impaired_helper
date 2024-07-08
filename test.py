import requests

api_key = "723ce630d2eb8321020251e9bcbb01a3"

def get_related_keywords(query, api_key):
    url = "https://dapi.kakao.com/v2/search/web"
    headers = {
        "Authorization": f"KakaoAK {api_key}"
    }
    params = {
        "query": query,
        "size": 10
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # 오류가 있으면 예외를 발생시킵니다.
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")  # 응답의 일부를 출력합니다.

        result = response.json()
        documents = result.get("documents", [])

        print(f"Number of documents: {len(documents)}")

        keywords = set()
        for doc in documents:
            title = doc.get("title", "")
            contents = doc.get("contents", "")
            keywords.update(title.split() + contents.split())

        # 입력 쿼리와 불용어 제거
        keywords = [word for word in keywords if word.lower() != query.lower() and len(word) > 1]

        return list(set(keywords))[:10]  # 상위 10개 키워드 반환

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return []

# 사용 예시
query = input("키워드를 입력하세요: ")
related_keywords = get_related_keywords(query, api_key)

print(f"'{query}'의 연관 키워드:")
for i, keyword in enumerate(related_keywords, 1):
    print(f"{i}. {keyword}")