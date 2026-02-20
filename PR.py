import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 데이터 로드 (파일 경로가 PR.py와 같은 폴더에 있어야 합니다)
file_path = 'Pediatric radiology.csv'
df = pd.read_csv(file_path)

# 2. 관련 키워드 설정 (주제 밀접도 판단용)
# 소아 MRI 준비, 진정제, 환자 경험 등과 관련된 키워드들입니다.
target_keywords = ['preparation', 'prepare', 'mock', 'simulation', 'virtual', 'vr',
                   'robot', 'sedation', 'anesthesia', 'anxiety', 'distress', 'child life']

def check_relevance(title):
    title_lower = str(title).lower()
    return any(k in title_lower for k in target_keywords)

# 관련 논문 여부 컬럼 추가
df['is_relevant'] = df['Title'].apply(check_relevance)

# 3. 연도별 통계 계산
# 연도별 전체 논문 수와 관련 논문 수를 집계합니다.
yearly_stats = df.groupby('Publication Year').agg(
    Total_Reviews=('Title', 'count'),
    Relevant_Reviews=('is_relevant', 'sum')
).reset_index()

# 4. 시각화 (Seaborn/Matplotlib 활용)
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")

# 전체 리뷰 논문 추이 (연한 색)
sns.barplot(data=yearly_stats, x='Publication Year', y='Total_Reviews',
            color='lightgray', label='Total Review Papers')

# 주제 관련 리뷰 논문 추이 (진한 색)
sns.barplot(data=yearly_stats, x='Publication Year', y='Relevant_Reviews',
            color='royalblue', label='Prep/Sedation Related Reviews')

plt.title('Trend of Review Papers in Pediatric Radiology (1977-2024)', fontsize=15)
plt.xlabel('Publication Year', fontsize=12)
plt.ylabel('Number of Papers', fontsize=12)
plt.xticks(rotation=45) # 연도가 겹치지 않게 회전
plt.legend()

plt.tight_layout()
plt.show()

# 5. 간단한 분석 결과 출력
latest_years = yearly_stats.tail(10)
print("--- 최근 10년 트렌드 요약 ---")
print(latest_years)