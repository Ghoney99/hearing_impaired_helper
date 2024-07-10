import streamlit as st
from openai import OpenAI
import nltk # New!!
from nltk.corpus import stopwords # New!!
from nltk.tokenize import sent_tokenize, word_tokenize # New!!
from nltk.probability import FreqDist # New!!
from heapq import nlargest

# #####################################################################
# # 제목 : Ai 튜터
# # 수정 날짜 : 2024-07-10
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
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    freq = FreqDist(words)
    ranking = {}
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in freq:
                if i in ranking:
                    ranking[i] += freq[word]
                else:
                    ranking[i] = freq[word]
    indexes = nlargest(num_sentences, ranking, key=ranking.get)
    return ' '.join([sentences[j] for j in sorted(indexes)])

def main():
    st.title("AI 튜터")
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "ft:gpt-3.5-turbo-0125:personal::9evZE1BR"
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 요약 기능 추가
    col1, col2 = st.columns(2)

    with col1:
        if st.button("강의 내용 요약"):
            file_path = 'text\lecture.txt'  # 강의 내용이 저장된 txt 파일 경로
            lecture_text = read_file(file_path)
            summary = summarize_text(lecture_text, num_sentences=3)
            st.write("강의 요약:")
            st.write(summary)

    with col2:
        if st.button("알림장"):
            file_path = 'text\lecture2.txt'  # 강의 내용이 저장된 txt 파일 경로
            lecture_text = read_file(file_path)
            summary = summarize_text(lecture_text, num_sentences=3)
            st.write("숙제 요약:")
            st.write(summary)

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