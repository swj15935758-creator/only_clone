# day15_basic.py
# 주제:day15 Basic 과제 - 공공도서관 대출 데이터 EDA
from python.print_util import pp
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# 그래프 기본 설정
sns.set_theme(style="whitegrid")
# 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic' # Windows: 나눔고딕
elif os_name == "Darwin":
    plt.rcParams["font.family"] = "AppleGothic"    # macOS: 애플고딕
elif os_name == "Linux":
    plt.rcParams["font.family"] = "NanumGothic"    # Linux: 나눔고딕

# [상황]
# day15_basic_data.csv에는 공공도서관의 도서 대출 기록이 저장되어 있습니다.
# 일부 값에는 공백, 표기 불일치, 결측치와 중복이 포함되어 있습니다.

# 경로
BASE_DIR = Path(__file__).parent # 현재 경로의 상위 경로
DATA_FILE = BASE_DIR /'..'/ 'assets' / 'day15_basic_data.csv' # CSV 파일 경로
OUTPUT_DIR = Path(__file__).with_name('day15_ouput') # 결과 파일 저장 디렉토리
OUTPUT_DIR.mkdir(exist_ok=True)


# [요구사항]
# CSV를 읽고 행·열 수, 자료형, 결측치 개수, 중복 건수를 출력하세요.
df = pd.read_csv(DATA_FILE,encoding='utf-8-sig')
pp('(행,열) :',df.shape)
pp('자료형 :',df.dtypes)
pp('결측치 개수 :',df.isna().sum())
pp('중복건수: ',df.duplicated().sum())

# 장르, 대출상태 컬럼의 앞뒤 공백을 제거하세요.
clean_df = df.copy()
clean_df['장르'] = clean_df['장르'].str.strip()
clean_df['대출상태'] = clean_df['대출상태'].str.strip()

# 소설 과 fiction은 소설로, 반납완료는 반납으로 통일하세요.
clean_df['대출상태'] = clean_df['대출상태'].replace({
    '반납완료': '반납',
})
clean_df['장르'] = clean_df['장르'].replace({
    'fiction': '소설',
})
# pp(clean_df) # 검증용 코드

# 대출일을 datetime으로 변환하고 변환 실패 행은 제거하세요.
clean_df['대출일']= pd.to_datetime(clean_df['대출일'],errors='coerce')
clean_df = clean_df.dropna(subset=['대출일'])
# 대출일수를 숫자로 변환하고 결측치는 전체 중앙값으로 대체하세요.
clean_df['대출일수']= pd.to_numeric(clean_df['대출일수'])
avg_look_days= clean_df['대출일수'].median()
clean_df['대출일수']= clean_df['대출일수'].fillna(avg_look_days)
pp(clean_df)
# 대출ID 기준 중복은 마지막 행을 남기고 제거하세요.
clean_df = clean_df.drop_duplicates(subset='대출ID', keep='last')
# 다음 KPI 3개를 계산하세요.
# 전체 대출 건수
total_book = len(clean_df)
# 반납 완료율
book_return_rate = (
    clean_df['대출상태'].eq('반납').mean() * 100
)
pp(book_return_rate.sum()) #9개
# 평균 대출일수
# 장르별 대출 건수와 평균 대출일수를 집계하세요.
summary = (
    clean_df.groupby('장르')
    .agg(
        대출건수 = ('대출ID', 'count'),
        평균대출일수 = ('대출일수', 'mean'),
    )
)
pp(summary)
# 장르별 대출 건수 막대그래프와 대출일수 히스토그램을 작성하세요.
fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(
    data = summary,
    x = '장르',
    y = '대출건수',
    color = 'C0',
    ax = ax
)
fig, ax = plt.subplots(figsize=(9, 5))
sns.histplot(
    data = clean_df,
    x='대출일수',  # 엑스 축 컬럼
    bins=8,  # 구간수
    kde=True,
    ax=ax,
)
plt.show()
# 가장 많이 대출된 장르와 평균 대출일수가 가장 긴 장르를 포함해 3줄 인사이트를 출력하세요.
top_genre = summary['대출건수'].idxmax()
longest_genre = summary['평균대출일수'].idxmax()

top_genre_count = summary.loc[top_genre, '대출건수']
longest_days = summary.loc[longest_genre, '평균대출일수']

pp('[인사이트]')

pp(f'1. {top_genre} 장르가 {top_genre_count}건으로 가장 많이 대출되어 '
    f'이용자의 대출 수요가 가장 높은 장르로 나타났습니다.')

pp(f'2. {longest_genre} 장르의 평균 대출일수가 {longest_days:.1f}일로 가장 길어 '
    f'다른 장르보다 비교적 오래 대출하는 경향이 나타났습니다.')

pp(f'3. 전체 평균 대출일수는 {avg_look_days:.1f}일이며, '
    f'장르에 따라 대출 기간에 차이가 나타나는지 추가 비교할 필요가 있습니다.')
