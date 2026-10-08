# day14_challenge.py
# 주제:day14 Challenge 과제 - 도시 대기질 EDA 대시보드
# 가상의 60일 대기질 데이터를 생성해 2×2 EDA 대시보드를 작성한다.
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
# NumPy 난수 시드를 100으로 고정한다.
np.random.seed(100)
# 60일의 날짜 데이터를 생성한다.
n=60
# 지역은 강남, 종로, 마포 중 하나가 반복되도록 구성한다.
df = pd.DataFrame({
    # 3개 직무 중 무작위 선택
    "지역": np.random.choice(
        ["강남", "종로", "마포"],
        size=n
    ),
# 다음 컬럼을 생성한다.
# 기온: 8~30도 범위
    "기온": np.random.uniform(
        low=8,
        high=30,
        size=n
    ),
# 풍속: 0.5~6.0 범위
    "풍속": np.random.uniform(
        low=0.5,
        high=6.0,
        size=n
    ),
# PM2.5: 10~80 범위
    "PM2.5": np.random.uniform(
        low=10,
        high=80,
        size=n
    ),

})
# PM10: PM2.5보다 큰 값이 되도록 생성
df['PM10'] = df['PM2.5'] + np.random.uniform(
    low=5,
    high=30,
    size=n
)
pp(df)
# DataFrame을 생성하고 각 컬럼의 기초통계를 출력한다.
# 날짜별 PM2.5 선그래프를 작성한다.
# 지역별 평균 PM2.5 막대그래프를 작성한다.
# PM2.5 히스토그램과 KDE를 작성한다.
# 풍속(X축)과 PM2.5(Y축)의 산점도를 작성하고 지역을 hue로 구분한다.
# 위 네 그래프를 2×2 형태의 하나의 Figure에 배치한다.
# 전체 Figure 제목은 "도시 대기질 EDA"로 지정한다.
# 완성된 Figure를 air_quality_dashboard.png 파일로 저장한다.
# 다음 내용을 콘솔에 출력한다.
# PM2.5 평균
# PM2.5 최대값이 발생한 날짜와 지역
# 지역별 평균 PM2.5
# 그래프에서 관찰되는 특징을 최소 4문장으로 작성한다.
# 풍속과 PM2.5의 관계가 보이더라도 인과관계로 단정할 수 없는 이유를 한 문장으로 작성한다.
