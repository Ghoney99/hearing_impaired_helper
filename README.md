# VONDI: 청각장애 학생을 위한 AI 디지털교과서 기반 학습 보조 솔루션

<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdYqpJW%2FbtsI5zeSeDL%2FMCxKkLYZQwwkQvZEtaG65k%2Fimg.png" alt="VONDI 로고" width="500"/>

## 📋 프로젝트 개요

VONDI는 청각장애 학생들의 학습 접근성을 높이고 교육 격차를 해소하기 위한 AI 기반 솔루션입니다. AI 디지털 교과서 환경에서 청각장애 학생들이 효과적으로 학습할 수 있도록 다양한 기능을 제공합니다.

## 🎯 주요 기능

### 1. AI 속기사
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fbh3lug%2FbtsI7OOILRq%2F1j7FnazaCslDO96rcHh140%2Fimg.png" alt="속기사" width="800"/>
- 실시간 음성-텍스트 변환 (STT)
- 자연어 처리(NLP)를 통한 자연스러운 자막 제공


### 2. AI 비서
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F03vGm%2FbtsI5OQq3n2%2FP5a8udwe4LlywItRUNC0P0%2Fimg.png" alt="비서1" width="800"/>
- 스마트 알림장: 중요 단어 정리 및 날짜/과목별 분류
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FvzVHb%2FbtsI5x2nJcl%2F8AXo5Do3KrqdfFQ3AbkSV1%2Fimg.png" alt="비서2" width="800"/>
- 수업 도우미: 수업 내용 저장, 요약본 및 Q&A 제공

### 3. 수어 번역 기능
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FKgsxz%2FbtsI7LqVoVv%2F7n5b9kIniD6XgGpWLDjsh0%2Fimg.png" alt="번역" width="800"/>
- LSTM 기반 실시간 수어 인식 및 텍스트 변환

### 4. 수어 사전
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FmQORo%2FbtsI5rOJvGQ%2FXWpScixkkUVLJhLglDasxK%2Fimg.png" alt="사전1" width="800"/>
- 국립국어원 수어 영상 API 연동
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbIL58N%2FbtsI5W8R5LV%2FJJc1fsNJcXn1JAwBeQ52b1%2Fimg.png" alt="사전2" width="800"/>
- 수어 단어 검색 및 영상 제공

## 🛠 기술 스택

- Frontend: ![Streamlit](https://img.shields.io/badge/streamlit-{#FF4B4B}?style=flat-square&logo=Python&logoColor=white)
- Backend: ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white)
- AI/ML: ![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white)
- API: 국립국어원 수어 영상 API, speech_recognition, OpenAI, nltk

## 🚀 시작하기

```bash
# 저장소 클론
git clone https://github.com/Ghoney99/hearing_impaired_helper.git

# 의존성 설치
pip install -r requirements.txt

# 서비스 실행
streamlit run app.py
```

## 📊 서비스 구성도

<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F94EMQ%2FbtsI5TYE6dk%2FcTaTNXY6LP7crrTPtnCOjK%2Fimg.png" alt="서비스구성도" width="800"/>

## 💻 인프라 구성도

<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FpufO6%2FbtsI5vKmGBI%2FB06CDCfhgGEzlmDl5Ocvjk%2Fimg.png" alt="인프라구성도" width="800"/>

## 📈 기대효과

1. 교육 격차 해소
   - 청각장애 학생의 학습 성과 개선
   - 비장애 학생과의 교육 기회 평등화

2. 경제적 효과
   - 학생 1인당 약 160만원 비용 절감
   - 15년간 약 700억원의 예산 절감 예상


VONDI - 모두를 위한 평등한 교육 환경을 만들어갑니다.
