import streamlit as st
from openai import OpenAI
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from heapq import nlargest

#####################################################################
# 제목 : AI 비서
# 수정 날짜 : 2024-07-24
# 작성자 : 장재혁
# 수정자 : 장지헌
# 수정 내용 : 챗봇 스타일 변경
#####################################################################

# NLTK 데이터 다운로드 (처음 실행 시 한 번만 필요)
nltk.download('punkt')
nltk.download('stopwords')

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

def extract_content(text):
    homework_start = text.find("숙제")
    if homework_start == -1:
        return text, ""
    lecture = text[:homework_start].strip()
    homework = text[homework_start:].strip()
    return lecture, homework

def main():
    # st.set_page_config(page_title="AI비서 본디", layout="wide")
    
    st.markdown("""
    <style>
    .stApp {
        margin: 0 auto;
        font-family: Arial, sans-serif;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }
    .chat-message.user {
        background-color: #e6f3ff;
    }
    .chat-message.bot {
        background-color: #f0f0f0;
    }
    .chat-icon {
        width: 50px;
        height: 50px;
        margin-right: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("AI 비서")

    # OPENAI_API_KEY 만료
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "ft:gpt-3.5-turbo-0125:personal::9evZE1BR"
    if "messages" not in st.session_state:
        st.session_state.messages = []

    file_path = "text/lecture3.txt"
    text = read_file(file_path)
    lecture_text, homework_text = extract_content(text)

    for message in st.session_state.messages:
        with st.container():
            st.markdown(f"""
            <div class="chat-message {'user' if message['role'] == 'user' else 'bot'}">
                <img src="https://cdn-icons-png.flaticon.com/512/1995/1995574.png" class="chat-icon">
                <div>{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("수업 내용 요약"):
            lecture_summary = summarize_text(lecture_text, num_sentences=3)
            st.session_state.messages.append({"role": "assistant", "content": lecture_summary})
            st.experimental_rerun()
    with col2:
        if st.button("똑똑한 알림장"):
            homework_summary = summarize_text(homework_text, num_sentences=3) if homework_text else "숙제 내용이 없습니다."
            st.session_state.messages.append({"role": "assistant", "content": homework_summary})
            st.experimental_rerun()
    with col3:
        if st.button("모르는 내용 질문하기"):
            st.session_state.messages.append({"role": "assistant", "content": "무엇이 궁금하신가요? 질문해 주세요."})
            st.experimental_rerun()

    user_input = st.text_input("무엇을 도와드릴까요?", key="user_input")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("답변 생성 중..."):
            response = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            response_content = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    response_content += chunk.choices[0].delta.content
            st.session_state.messages.append({"role": "assistant", "content": response_content})
        st.experimental_rerun()
