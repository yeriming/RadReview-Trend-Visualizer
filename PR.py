import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# 1. 데이터 로드 및 중복 제거 (데이터 정제)
file_path = 'Pediatric radiology.csv'
df = pd.read_csv(file_path)

df = df.drop_duplicates(subset=['PMID'], keep='first')
df = df.drop_duplicates(subset=['Title'], keep='first')

# 2. 분석 지표 설정
# 주제 관련 키워드 (Topic)
target_keywords = ['preparation', 'prepare', 'mock', 'simulation', 'virtual', 'vr',
                   'robot', 'sedation', 'anesthesia', 'anxiety', 'distress', 'child life']

def classify_paper(title):
    title_lower = str(title).lower()
    is_topic_related = any(k in title_lower for k in target_keywords)
    is_scoping_method = 'scoping' in title_lower
    # 주제와 방법론의 교집합 (Intersection)
    is_intersection = is_topic_related and is_scoping_method
    return pd.Series([is_topic_related, is_scoping_method, is_intersection])

df[['Topic_Related', 'Scoping_Method', 'Intersection']] = df['Title'].apply(classify_paper)

# 3. 연도별 통계 집계
stats = df.groupby('Publication Year').agg(
    Total=('Title', 'count'),
    Topic=('Topic_Related', 'sum'),
    Methodology=('Scoping_Method', 'sum'),
    Intersection=('Intersection', 'sum')
).reset_index()

# 4. 시각화 (레이어링을 통한 분포 파악)
plt.figure(figsize=(15, 8))
sns.set_style("whitegrid")

# 레이어 1: 저널 전체 리뷰 수
sns.barplot(data=stats, x='Publication Year', y='Total', color='#E0E0E0', label='Total Reviews')

# 레이어 2: 특정 주제 관련 리뷰 (Topic Distribution)
sns.barplot(data=stats, x='Publication Year', y='Topic', color='#A2C2E1', label='Topic-Related Reviews')

# 레이어 3: 스코핑 리뷰 방법론 채택 수 (Methodological Distribution)
sns.barplot(data=stats, x='Publication Year', y='Methodology', color='#FFD54F', label='Scoping Methodology')

# 레이어 4: 두 요소의 교집합 (Intersection of Topic and Methodology)
sns.barplot(data=stats, x='Publication Year', y='Intersection', color='#D32F2F', label='Intersection')

plt.title('Statistical Distribution of Review Papers in Pediatric Radiology (1977-2024)', fontsize=16)
plt.xticks(rotation=45)
plt.legend(loc='upper left')
plt.tight_layout()

# 5. 자동 저장 (파일 이름에 일시 포함)
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
save_name = f"journal_trend_analysis_{timestamp}.png"
plt.savefig(save_name, dpi=300)
print(f"분석 결과 이미지가 저장되었습니다: {save_name}")

plt.show()

# 6. 통계 요약 출력
print(f"\n[데이터 통계 요약]")
print(f"- 분석 대상 총 논문 수: {len(df)}건")
print(f"- 주제 관련 리뷰: {df['Topic_Related'].sum()}건")
print(f"- 스코핑 방법론 리뷰: {df['Scoping_Method'].sum()}건")
print(f"- 주제-방법론 교집합: {df['Intersection'].sum()}건")