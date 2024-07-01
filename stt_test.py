import speech_recognition as sr

recognizer = sr.Recognizer()

def speech_to_text():
    with sr.Microphone() as source:
        print("말씀해주세요...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language='ko-KR')
        print(f"인식된 텍스트: {text}")
        return text
    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        print(f"음성 인식 서비스에 접근할 수 없습니다: {e}")

# 테스트
while True:
    result = speech_to_text()
    if result == "종료":
        break
