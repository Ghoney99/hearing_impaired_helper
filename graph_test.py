import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] ='Malgun Gothic'
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# CSV 파일 로드
df = pd.read_csv('student_scores_korean_subjects.csv')

# 학생 이름 설정
student_name = '최수아'

# 해당 학생의 데이터 선택
student_data = df[df['이름'] == student_name]

# 숫자 데이터로 변환할 수 있는 열 선택
numeric_columns = ['국어_중간고사', '국어_기말고사', '수학_중간고사', '수학_기말고사', '영어_중간고사', '영어_기말고사', '과학_중간고사', '과학_기말고사']

# 숫자로 변환할 수 없는 열 제거
student_data = student_data[numeric_columns].apply(pd.to_numeric, errors='coerce')

# 결측치(NaN)가 있는 행 제거
student_data = student_data.dropna()

# 학기 정보가 없으므로 '학기' 열을 임의로 생성
student_data['학기'] = range(1, len(student_data) + 1)

# 중간고사와 기말고사 평균 계산
avg_mid_scores = student_data.groupby('학기')[['국어_중간고사', '수학_중간고사', '영어_중간고사', '과학_중간고사']].mean().reset_index()
avg_final_scores = student_data.groupby('학기')[['국어_기말고사', '수학_기말고사', '영어_기말고사', '과학_기말고사']].mean().reset_index()

# 과목 리스트 정의
subjects = ['국어', '수학', '영어', '과학']

# 중간고사 평균 점수 리스트
avg_mid_scores_list = avg_mid_scores[['국어_중간고사', '수학_중간고사', '영어_중간고사', '과학_중간고사']].values.tolist()[0]

# 기말고사 평균 점수 리스트
avg_final_scores_list = avg_final_scores[['국어_기말고사', '수학_기말고사', '영어_기말고사', '과학_기말고사']].values.tolist()[0]

# 과목 개수
num_subjects = len(subjects)

# 오각형 그래프를 그리기 위한 각도 계산
angles = np.linspace(0, 2 * np.pi, num_subjects, endpoint=False).tolist()

# 첫 번째 각도를 다시 추가하여 폐곡선을 만듦
angles += angles[:1]

# 그림 크기 설정
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# 중간고사 오각형 그래프 그리기
ax.fill(angles, avg_mid_scores_list + avg_mid_scores_list[:1], color='blue', alpha=0.25)
ax.plot(angles, avg_mid_scores_list + avg_mid_scores_list[:1], color='blue', linewidth=2, label='중간고사')

# 기말고사 오각형 그래프 그리기
ax.fill(angles, avg_final_scores_list + avg_final_scores_list[:1], color='green', alpha=0.25)
ax.plot(angles, avg_final_scores_list + avg_final_scores_list[:1], color='green', linewidth=2, label='기말고사')

# 레이블 설정
ax.set_yticklabels([])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(subjects, fontsize=12)

# 제목 설정
ax.set_title(f'{student_name} 학생의 과목별 중간고사 vs 기말고사 평균 성적', size=20, y=1.1)

# 범례 추가
ax.legend(loc='upper right')

# 그리드 추가
ax.grid(True)

# 그래프 보여주기
plt.show()
