import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from heapq import nlargest

# NLTK 데이터 다운로드 (처음 실행 시 한 번만 필요)
nltk.download('punkt')
nltk.download('stopwords')

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def summarize_text(text, num_sentences=3):
    # 문장 토큰화
    sentences = sent_tokenize(text)
    
    # 불용어 제거 및 단어 토큰화
    stop_words = set(stopwords.words('english'))
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

# 사용 예시
file_path = 'lecture.txt'  # 강의 내용이 저장된 txt 파일 경로
lecture_text = read_file(file_path)
summary = summarize_text(lecture_text, num_sentences=3)
print(summary)