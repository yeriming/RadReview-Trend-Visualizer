import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# ==========================================
# 1. 설정 (Pediatric Radiology 전용)
# ==========================================
JOURNAL_NAME = 'Patient Education and Counseling'
FILE_PATH = f'{JOURNAL_NAME}.csv'

# ==========================================
# 2. 데이터 로드 및 중복 제거
# ==========================================
try:
    df = pd.read_csv(FILE_PATH)
    initial_count = len(df)
    # 데이터 무결성을 위해 PMID와 Title 기준 중복 제거
    df = df.drop_duplicates(subset=['PMID'], keep='first')
    df = df.drop_duplicates(subset=['Title'], keep='first')
    print(f"[{JOURNAL_NAME}] 중복 제거 완료: {initial_count}건 -> {len(df)}건")
except FileNotFoundError:
    print(f"오류: '{FILE_PATH}' 파일을 찾을 수 없습니다. 파일명을 확인해 주세요.")
    exit()

# ==========================================
# 3. 분석 키워드 및 판별 로직 (통일)
# ==========================================
# VR 제외 / sedation, MRI, social robot 포함
TARGET_KEYWORDS = [
    'preparation', 'prepare', 'mock', 'simulation', 'robot', 'social robot',
    'sedation', 'mri', 'magnetic resonance', 'anesthesia', 'anxiety',
    'distress', 'child life'
]

def analyze_paper(title):
    title_lower = str(title).lower()
    is_topic = any(k in title_lower for k in TARGET_KEYWORDS)
    is_method = 'scoping' in title_lower
    is_inter = is_topic and is_method
    return pd.Series([is_topic, is_method, is_inter])

# [중요] 여기서 Is_Topic 열이 생성됩니다.
df[['Is_Topic', 'Is_Method', 'Is_Intersection']] = df['Title'].apply(analyze_paper)

# ==========================================
# 4. 연도별 통계 집계
# ==========================================
stats = df.groupby('Publication Year').agg(
    Total=('Title', 'count'),
    Topic=('Is_Topic', 'sum'),
    Methodology=('Is_Method', 'sum'),
    Intersection=('Is_Intersection', 'sum')
).reset_index()

# ==========================================
# 5. 시각화 (라벨 및 색상 통일)
# ==========================================
plt.figure(figsize=(15, 8))
sns.set_style("whitegrid")

sns.barplot(data=stats, x='Publication Year', y='Total', color='#E0E0E0', label='Total Review Papers')
sns.barplot(data=stats, x='Publication Year', y='Topic', color='#A2C2E1', label='Thematic Reviews (MRI/Sedation/Robot)')
sns.barplot(data=stats, x='Publication Year', y='Methodology', color='#FFD54F', label='Scoping Review Methodology')
sns.barplot(data=stats, x='Publication Year', y='Intersection', color='#D32F2F', label='Intersectional Scholarship (Topic + Method)')

plt.title(f'Statistical Distribution of Review Papers in {JOURNAL_NAME} (1977-2024)', fontsize=16, fontweight='bold')
plt.xlabel('Publication Year', fontsize=12)
plt.ylabel('Number of Papers', fontsize=12)
plt.xticks(rotation=45)
plt.legend(loc='upper left', frameon=True)
plt.tight_layout()

# 이미지 자동 저장
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
journal_code = JOURNAL_NAME.replace(" ", "_")
plt.savefig(f"{journal_code}_Trend_Analysis_{timestamp}.png", dpi=300)

# ==========================================
# 6. 관련 논문 리스트 CSV 파일로 저장
# ==========================================
# Is_Topic 열이 생성된 후에 필터링을 수행하므로 KeyError가 발생하지 않습니다.
relevant_list = df[df['Is_Topic'] == True].copy()

if not relevant_list.empty:
    output_filename = f"{journal_code}_Relevant_Papers_{timestamp}.csv"
    # 한글 깨짐 방지를 위해 utf-8-sig 인코딩 사용
    relevant_list.to_csv(output_filename, index=False, encoding='utf-8-sig')
    print(f"\n[저장 성공] 관련 논문 {len(relevant_list)}건이 '{output_filename}'으로 저장되었습니다.")
else:
    print("\n[알림] 관련 키워드와 일치하는 논문이 없습니다.")

plt.show()