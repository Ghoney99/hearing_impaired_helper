import streamlit as st
from openai import OpenAI
import nltk # New!!
from nltk.corpus import stopwords # New!!
from nltk.tokenize import sent_tokenize, word_tokenize # New!!
from nltk.probability import FreqDist # New!!
from heapq import nlargest

# #####################################################################
# # 제목 : AI 비서
# # 수정 날짜 : 2024-07-11
# # 작성자 : 장재혁
# # 수정자 : 장지헌
# # 수정 내용 : 강의록 요약 및 알림장 기능 추가
# #####################################################################


# # NLTK 데이터 다운로드 (처음 실행 시 한 번만 필요)
# nltk.download('punkt')
# nltk.download('stopwords')

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

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

def main():
    st.title("AI 비서")
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "ft:gpt-3.5-turbo-0125:personal::9evZE1BR"
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 요약 기능 추가
    col1, col2 = st.columns(2)

    # 파일에서 텍스트 읽기
    file_path = "text\lecture3.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # 강의와 숙제 부분 추출
    lecture_text, homework_text = extract_content(text)

    
    with col1:
        if st.button("강의 내용 요약"):
            lecture_summary = summarize_text(lecture_text, num_sentences=3)
            st.write(lecture_summary)

    with col2:
        if st.button("알림장"):
            homework_summary = summarize_text(homework_text, num_sentences=3) if homework_text else "숙제 내용이 없습니다."
            st.write(homework_summary)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})