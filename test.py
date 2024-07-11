import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from heapq import nlargest

# NLTK 데이터 다운로드 (처음 한 번만 실행하면 됩니다)
nltk.download('punkt')
nltk.download('stopwords')

def summarize_text(text, num_sentences=3):
    # 문장 토큰화
    sentences = sent_tokenize(text)
    
    # 불용어 제거 및 단어 토큰화
    stop_words = set(stopwords.words('english'))  # 한국어 불용어 목록이 없으므로 영어로 대체
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    
    # 단어 빈도 계산
    freq = FreqDist(words)
    
    # 문장 점수 계산
    ranking = {}
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in freq:
                if i in ranking:
                    ranking[i] += freq[word]
                else:
                    ranking[i] = freq[word]
    
    # 상위 n개 문장 선택
    indexes = nlargest(num_sentences, ranking, key=ranking.get)
    
    # 선택된 문장들을 원래 순서대로 정렬
    return ' '.join([sentences[j] for j in sorted(indexes)])

def extract_content(text):
    homework_start = text.find("숙제")
    if homework_start == -1:
        return text, ""
    lecture = text[:homework_start].strip()
    homework = text[homework_start:].strip()
    return lecture, homework

# 파일에서 텍스트 읽기
file_path = "text\lecture3.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# 강의와 숙제 부분 추출
lecture_text, homework_text = extract_content(text)

# 강의 요약
lecture_summary = summarize_text(lecture_text, num_sentences=3)

# 숙제 요약
homework_summary = summarize_text(homework_text, num_sentences=3) if homework_text else "숙제 내용이 없습니다."

print("강의 요약:", lecture_summary)
print("\n숙제 요약:", homework_summary)