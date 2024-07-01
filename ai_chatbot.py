import streamlit as st
from openai import OpenAI

#####################################################################
# 제목 : Ai 튜터
# 수정 날짜 : 2024-07-01
# 작성자 : 장재혁
# 수정자 : 장재혁
# 수정 내용 : 파일 생성
#####################################################################

def main():
    st.title("AI 튜터")
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "ft:gpt-3.5-turbo-0125:personal::9evZE1BR"

    if "messages" not in st.session_state:
        st.session_state.messages = []

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