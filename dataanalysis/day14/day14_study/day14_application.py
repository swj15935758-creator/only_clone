# day14_application.py
# 주제:day14 Application 과제 - 채용 평가 데이터 시각화
#
# 가상의 채용 평가 데이터를 생성하고 지원자의 평가 결과를 시각적으로 분석한다.
import platform # 운영체제 정보 확인
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from python.print_util import pp
# 그래프 기본 설정
sns.set_theme(style="whitegrid")  # 흰 배경에 격자선 표시하는 테마
if platform.system() == 'Windows':  # 윈도우라면
    plt.rcParams['font.family'] = ['Malgun Gothic']  # 한글 폰트 설정
elif platform.system() == 'Darwin':  # macOS라면
    plt.rcParams['font.family'] = ['AppleGothic']
elif platform.system() == 'Linux':  # 리눅스라면
    plt.rcParams['font.family'] = ['NanumGothic']

plt.rcParams['axes.unicode_minus'] = False  # 음수 기호 (-) 깨짐 방지 설정
# 요구사항
# NumPy 난수 시드를 42로 고정한다.
# 지원자 60명의 데이터를 다음 기준으로 생성한다.
# 직무: Backend, Frontend, Data 중 하나
# 코딩점수: 평균 72, 표준편차 12의 정규분포
# 면접점수: 평균 75, 표준편차 10의 정규분포
# 난수 시드 고정
n=60
np.random.seed(42)
# 데이터프레임 생성
df = pd.DataFrame({
    # 3개 직무 중 무작위 선택
    "직무": np.random.choice(
        ["Backend", "Frontend", "Data"],
        size=n
    ),

    # 평균 72, 표준편차 12의 정규분포
    "코딩점수": np.random.normal(
        loc=72,
        scale=12,
        size=n
    ),

    # 평균 75, 표준편차 10의 정규분포
    "면접점수": np.random.normal(
        loc=75,
        scale=10,
        size=n
    )
})
# pp(df)
# def clean_text(series):
#     return (
#         series.astype("string")
#         .str.strip()
#         .str.replace(r"\s+", " ", regex=True)
# )
#
#
# def iqr_bounds(series):
#     q1 = series.quantile(0.25)
#     q3 = series.quantile(0.75)
#     iqr = q3 - q1
#     return q1 - 1.5 * iqr, q3 + 1.5 * iqr
# 코딩점수와 면접점수는 0~100 범위로 제한한다.
# cd_lower,cd_upper = iqr_bounds(df['코딩점수'])
df['코딩점수'] = df['코딩점수'].clip(lower=0, upper=100)
# meet_lower,meet_upper = iqr_bounds(df['면접점수'])
df['면접점수'] = df['면접점수'].clip(lower=0, upper=100)


# 최종점수 = 코딩점수 × 0.6 + 면접점수 × 0.4 로 계산한다.
df['최종점수'] = df['코딩점수'] * 0.6 + df['면접점수'] * 0.4
# 최종점수가 75점 이상이면 합격, 아니면 불합격으로 판정한다.
df.loc[(df['최종점수'] >= 75),'합격여부'] = '합격'
df.loc[(df['최종점수'] < 75),'합격여부'] = '불합격'
# Seaborn을 사용해 최종점수 히스토그램과 KDE를 작성한다.
fig,ax = plt.subplots(figsize=(8,5))

sns.histplot(
    data=df, # 데이터 프레임
    x = '최종점수', # 엑스 축 컬럼
    bins=8, # 구간수
    kde=True,
    ax=ax,
)
ax.set_title('최종점수 분포')
ax.set_xlabel('최종점수')
ax.set_ylabel('빈도')
fig.tight_layout()
# 코딩점수(X축)와 면접점수(Y축)의 산점도를 작성하고 합격여부를 hue로 구분한다.
fig,ax = plt.subplots(figsize=(8,5))

sns.scatterplot(
    data=df, # 데이터 프레임
    x = '코딩점수', # 엑스 축 컬럼
    y = '면접점수',
    hue='합격여부',
    s = 90, # 점의 크기
    alpha=0.5, # 점의 투명도
    ax=ax,
)
ax.set_title('합격여부')
ax.set_xlabel('코딩점수')
ax.set_ylabel('면접점수')
fig.tight_layout()
# 직무별 평균 최종점수를 막대그래프로 작성한다.

fig,ax = plt.subplots(figsize=(8,5))

sns.barplot(
    data=df, # 데이터 프레임
    x = '직무', # 엑스 축 컬럼
    y = '최종점수', # 와이 축 컬럼
    estimator='mean', # 평균 막대 높이로 사용
    errorbar=None,
    ax=ax,
)
ax.set_title('직무별 최종점수 평균')
ax.set_xlabel('직무')
ax.set_ylabel('최종점수')
fig.tight_layout()

# 세 그래프에 제목과 축 이름을 지정한다.
# 전체 합격률과 직무별 평균 최종점수를 출력한다.
pass_rate = (df['합격여부'] == '합격').mean() * 100
print(f'전체 합격률: {pass_rate:.1f}%')

job_mean = df.groupby('직무')['최종점수'].mean()
pp(job_mean)
# 그래프에서 확인할 수 있는 특징을 3문장 이내로 출력한다.
print('최종점수는 특정 구간에 많이 분포되어 있다.')
print('코딩점수와 면접점수가 높을수록 합격자가 많이 나타난다.')
print('직무별 평균 최종점수에는 차이가 있다.')
# plt.show()
