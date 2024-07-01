import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# 글꼴 설정
plt.rcParams['font.family'] ='Malgun Gothic'

def compare_student_with_average(df, student_id):
        student_data = df[df['학생ID'] == student_id]

        df['전체_평균_국어'] = df[['국어_중간고사', '국어_기말고사']].mean(axis=1)
        df['전체_평균_수학'] = df[['수학_중간고사', '수학_기말고사']].mean(axis=1)
        df['전체_평균_영어'] = df[['영어_중간고사', '영어_기말고사']].mean(axis=1)
        df['전체_평균_과학'] = df[['과학_중간고사', '과학_기말고사']].mean(axis=1)

        semester_avg = df.groupby('학기').mean(numeric_only=True).reset_index()

        student_data['학생_평균_국어'] = student_data[['국어_중간고사', '국어_기말고사']].mean(axis=1)
        student_data['학생_평균_수학'] = student_data[['수학_중간고사', '수학_기말고사']].mean(axis=1)
        student_data['학생_평균_영어'] = student_data[['영어_중간고사', '영어_기말고사']].mean(axis=1)
        student_data['학생_평균_과학'] = student_data[['과학_중간고사', '과학_기말고사']].mean(axis=1)

        student_avg = student_data.groupby('학기').mean(numeric_only=True).reset_index()

        fig, axs = plt.subplots(2, 2, figsize=(14, 10))
        subjects = ['국어', '수학', '영어', '과학']
        for i, subject in enumerate(subjects):
            ax = axs[i // 2, i % 2]
            ax.plot(semester_avg['학기'], semester_avg[f'전체_평균_{subject}'], label='전체 평균', marker='o')
            ax.plot(student_avg['학기'], student_avg[f'학생_평균_{subject}'], label='학생 평균', marker='o')
            ax.set_title(f'{subject} 성적 비교')
            ax.set_xlabel('학기')
            ax.set_ylabel('평균 성적')
            ax.legend()

        plt.tight_layout()
        st.pyplot(fig)


def main():
    st.title("최수아")
    st.write("성적 확인")
    df = pd.read_csv('student_scores_korean_subjects.csv')
    for col in ['국어_중간고사', '국어_기말고사', '수학_중간고사', '수학_기말고사', '영어_중간고사', '영어_기말고사', '과학_중간고사', '과학_기말고사']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 학생 이름과 ID를 매핑
    student_name_to_id = {row['이름']: row['학생ID'] for _, row in df.iterrows()}
    student_id = student_name_to_id['최수아']
    compare_student_with_average(df, student_id)
    

