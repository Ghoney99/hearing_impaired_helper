import speech_recognition as sr
import streamlit as st
#####################################################################
# 제목 : STT
# 수정 날짜 : 2024-07-01
# 작성자 : 장지헌
# 수정자 : 장재혁
# 수정 내용 : stt 파일생성
#####################################################################

# STT 함수
def speech_to_text(recognizer):
    with sr.Microphone() as source:
        st.write("[자막]")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language='ko-KR')
        st.write(f"{text}") # 결과값 출력
        return text
    except sr.UnknownValueError:
        st.write("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        st.write(f"음성 인식 서비스에 접근할 수 없습니다: {e}")


# def main():
#     st.title("Speech-to-Text (STT) App")
#     st.write("STT 관련 콘텐츠")
#     # Recognizer 객체 생성
#     recognizer = sr.Recognizer()

#     # Streamlit 애플리케이션 정의
#     st.title("마이크로부터 텍스트로 변환하기")

#     st.write("마이크를 통해 음성을 입력하고 '인식' 버튼을 클릭하세요.")

#     if st.button("인식"):
#         result = speech_to_text(recognizer)
# #####################################################################