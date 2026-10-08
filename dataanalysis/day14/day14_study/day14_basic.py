# day14_basic.py
# 주제:ay14 Basic 과제 - 도서관 대출 현황 시각화
#
# 다음 데이터는 1월부터 6월까지의 도서관 장르별 대출 건수이다.

import platform # 운영체제 정보 확인
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# 1. 데이터 프레임 으로 만듬
df=pd.DataFrame({
    '월': ['1월', '2월', '3월', '4월', '5월', "6월"],
    '소설': [120, 135, 128, 150, 164, 172],
    'IT': [80, 95, 110, 118, 125, 140],
    '경제': [65, 72, 78, 85, 92, 98]
})

# 2. 대출 건수 계산
df['월별대출건수'] =(df[['소설','IT','경제']].sum(axis=1))
pp(df[['월','월별대출건수']])

# 위 데이터를 Pandas DataFrame으로 생성한다.
# 월별 전체 대출 건수를 계산한다.
# 월별 전체 대출 건수를 선그래프로 작성한다.
# 장르별 6개월 총대출 건수를 계산한다.
fig, ax = plt.subplots(figsize=(9,5))
ax.plot( # 선 그래프
    df['월'], #x 축
    df['월별대출건수'], # y축
    marker='o', # 데이터 위치 표시
    linewidth=2, # 넓이
    label='월별 총 대출 권수' # 범례에 표시될 이름
)
ax.set_title('월별 대출권수')
ax.set_xlabel('월')
ax.set_ylabel('대출')
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout() # 그래프 내의 요소들이 겹치지 않게 설정
# plt.show()


# 장르별 총대출 건수를 막대그래프로 작성한다.
# 모든 그래프에 제목, X축 이름, Y축 이름을 표시한다.
# 막대그래프에는 각 막대의 값을 표시한다.

genre_sum = df[['소설','IT','경제']].sum()

fig, ax = plt.subplots(figsize=(8,5))
bars = ax.bar(
    genre_sum.index,
    genre_sum.values
)
ax.set_title('장르별 총대출 비교')
ax.set_xlabel('장르')
ax.set_ylabel('총대출건수')
ax.bar_label( # 각 막대의 레이블
    bars, # 막대 그래프 객체
    fmt='%.0f', # 레이블의 형식 : 소수점 없이 숫자 출력
)
fig.tight_layout()
plt.show()

# 두 그래프에서 확인할 수 있는 특징을 각각 한 문장으로 출력한다.
print('월별 전체 대출 건수는 전체적으로 증가하는 추세이다.')
print('장르별 총대출 건수는 소설이 가장 많고 경제가 가장 적다.')