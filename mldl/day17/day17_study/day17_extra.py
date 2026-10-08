# #day17_extra - 서울 공공자전거 대여수요 다중회귀 분석 실습
#
# [실습 주제]
# 서울 공공자전거의 시간대별 대여수요를 날씨와 시간 정보를 이용해 예측하기
#
# [데이터]
# - 데이터 파일: SeoulBikeData_ko.csv
# - 데이터명: Seoul Bike Sharing Demand
# - 제공기관: UCI Machine Learning Repository
# - 데이터 건수: 8,760건
# - 분석 유형: Regression(회귀)
# - 결측값: 없음
# - 대상 기간: 2017년 12월 ~ 2018년 11월
# - 목표변수: 대여량(시간당 대여 자전거 수)
# - 공식 출처:
#   https://archive.ics.uci.edu/dataset/560/seoul+bike+sharing+demand
#
# [파일 구성]
# day17/
# ├─ day17_extra.py
# └─ assets/
#    └─ SeoulBikeData_ko.csv
from operator import index

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from include.graph_config import set_graph
from python.print_util import pp
from python.print_util import pp

# [컬럼 설명]
# 날짜        : 측정 날짜
# 대여량      : 시간당 대여 자전거 수
# 시간        : 시간(0~23)
# 기온        : 기온(°C)
# 습도        : 상대습도(%)
# 풍속        : 풍속(m/s)
# 가시거리    : 가시거리(10m 단위)
# 이슬점온도  : 이슬점 온도(°C)
# 일사량      : 일사량(MJ/m²)
# 강수량      : 강수량(mm)
# 적설량      : 적설량(cm)
# 계절        : Spring, Summer, Autumn, Winter
# 휴일        : Holiday, No Holiday
# 운영여부    : Yes, No
#
# [분석 목표]
# 여러 개의 독립변수를 동시에 사용하는 다중선형회귀 모델을 생성하고,
# 날씨·시간·계절·휴일 정보가 서울 공공자전거 대여수요를 어느 정도 설명하는지 분석합니다.
# 모델의 성능은 MAE, MSE, RMSE, R²를 이용해 평가하고,
# 실제값과 예측값 및 잔차를 시각화하여 모델의 한계까지 확인합니다.
#
# [실습 과제]
#
# SeoulBikeData_ko.csv를 pandas DataFrame으로 불러온 뒤 데이터의 전체 크기, 앞부분 데이터,
# 컬럼별 데이터 타입을 확인하세요. 이어서 각 컬럼의 결측값 개수와 전체 중복행 개수를 확인하여
# 분석 전에 데이터 상태를 파악하세요.
SeoulBikeData_ko_csv_dir = 'assets/SeoulBikeData_ko.csv'
df = pd.read_csv(SeoulBikeData_ko_csv_dir)
# df.info()
clean_df = df.copy()
# pp(clean_df.isna().sum()) #없음
# pp(clean_df.duplicated(keep=False).sum()) # 없음
# pp(clean_df.describe()) # 통계
# 날짜 컬럼을 datetime 타입으로 변환한 후 월과 요일 정보를 새로운 컬럼으로 생성하세요.
clean_df['날짜'] = pd.to_datetime(clean_df['날짜'],format='%d/%m/%Y',errors='coerce')
clean_df['월'] = clean_df['날짜'].dt.month
# 요일은 월요일을 0, 화요일을 1, ..., 일요일을 6으로 표현합니다.
clean_df['요일'] = clean_df['날짜'].dt.dayofweek
# 운영여부가 Yes인 데이터만 선택하여 정상적으로 서비스가 운영된 시간대의 대여수요만 분석하세요.
# 운영되지 않은 시간에 기록된 0은 실제 수요 부족이 아니라 서비스 중단의 결과일 수 있기 때문입니다.
is_running = clean_df['운영여부'].eq('Yes')
# pp(is_running.sum())
running = clean_df[is_running]
# pp(running)
running_sum_gp = ((
    running
    .groupby('시간')['대여량']
    .sum()
).reset_index()
.sort_values(
    by = '시간',
    ascending = True
))
# pp(running_mean_gp)
# 정상 운영 데이터에서 시간대별 평균 대여량을 계산하고 선그래프로 시각화하세요.
# x축에는 시간을, y축에는 평균 대여량을 표시하고 하루 중 대여수요가 집중되는 시간대를 확인하세요.
# 특히 출퇴근 시간대에 평균 대여량이 증가하는지 그래프를 통해 분석하세요.
running_mean_gp = ((
    running
    .groupby('시간')['대여량']
    .mean()
).reset_index()
.sort_values(
    by = '시간',
    ascending = True
))

set_graph(10, 8, 13)
plt.plot(running_mean_gp)
plt.xlabel('시간별')
plt.ylabel('대여량')
# plt.show()
#
# 기온과 대여량의 관계를 산점도로 시각화하세요.
# x축에는 기온, y축에는 대여량을 배치하고 기온이 높아질수록 대여량이 어떤 경향을 보이는지 확인하세요.
# 점이 많이 겹치므로 투명도를 적절히 설정하여 전체 분포를 확인할 수 있도록 작성하세요.
plt.scatter(
    data = running,
    x='기온',
    y='대여량',
    s= 10,
    alpha = 0.5,
)
plt.xlabel('기온별')
plt.ylabel('대여량')
# plt.show()

# 다중회귀 모델의 독립변수로 시간, 기온, 습도, 풍속, 가시거리, 일사량, 강수량,
X=clean_df[['시간','기온','습도','풍속','가시거리','일사량','강수량','적설량','월','요일','계절','휴일']]
y=clean_df['대여량']
# 적설량, 월, 요일을 사용하세요. 계절과 휴일도 독립변수에 포함하되 문자열 데이터이므로
# pd.get_dummies()를 사용하여 더미변수로 변환하세요.
# 더미변수 생성 시 drop_first=True와 dtype=int를 사용하세요.
# 종속변수는 시간당 자전거 대여량으로 지정합니다.
X = pd.get_dummies(
    X,
    columns=['계절','휴일'],
    drop_first=True,
    dtype=int
)

# 이슬점온도는 기온과 매우 높은 상관관계를 가질 가능성이 있으므로 이번 모델의 독립변수에서는 제외하세요.
# 이는 서로 매우 유사한 정보를 가진 변수가 동시에 모델에 포함될 때 발생할 수 있는
# 다중공선성(Multicollinearity)의 영향을 줄이기 위한 간단한 선택입니다.

# 전처리가 완료된 독립변수 X와 종속변수 y를 학습용 80%, 테스트용 20%로 분리하세요.
# train_test_split()의 test_size는 0.2, random_state는 42로 지정하여
# 실행할 때마다 동일한 분할 결과를 얻을 수 있도록 하세요.
RANDOM_STATE = 42
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size= 0.2,
    random_state= RANDOM_STATE,
)
# LinearRegression 모델을 생성한 뒤 학습 데이터로 다중선형회귀 모델을 학습하세요.
pp(df['날짜'].head(10))
pp(clean_df[['날짜','월','요일']].head())
pp(clean_df[['날짜','월','요일']].isna().sum())
multi_model = LinearRegression()
multi_model.fit(X_train,y_train)
pred = multi_model.predict(X_test)
pp(pred)
multi_model = LinearRegression()
multi_model.fit(X_train,y_train)
pred = multi_model.predict(X_test)
pp(pred)
# 테스트 데이터의 대여량을 예측하고 MAE, MSE, RMSE, R²를 계산하세요.
# MAE는 평균적으로 몇 대 정도의 예측 오차가 발생하는지,
# RMSE는 큰 예측 오류까지 고려했을 때 오차가 어느 정도인지,
# R²는 모델이 실제 대여량 변동을 얼마나 설명하는지를 중심으로 해석하세요.
#
# 실제대여량, 예측대여량, 오차, 절대오차로 구성된 DataFrame을 작성하고 앞 10개의 결과를 확인하세요.
# 또한 모델의 절편과 각 독립변수의 회귀계수를 DataFrame으로 정리하고
# 각 계수가 양수인지 음수인지 확인하세요.
# 각 독립변수는 서로 단위가 다르므로 회귀계수의 절댓값만 비교하여
# 어떤 변수가 가장 중요하다고 단정하지 않도록 주의하세요.
#
# 실제 대여량을 x축, 예측 대여량을 y축으로 하는 산점도를 작성하고
# 실제값과 예측값이 완전히 같은 위치를 나타내는 y=x 기준선을 함께 표시하세요.
# 점들이 이 기준선 주변에 모여 있을수록 실제값과 예측값이 비슷하다고 해석할 수 있습니다.
#
# 잔차를 실제값 - 예측값으로 계산한 뒤 예측 대여량을 x축, 잔차를 y축으로 산점도를 작성하세요.
# 잔차가 0인 위치에 수평 기준선을 표시하고 점들이 0을 중심으로 무작위로 분포하는지 확인하세요.
# 곡선이나 특정한 형태의 패턴이 남는다면 선형회귀가 데이터의 비선형적인 구조를
# 충분히 설명하지 못하고 있을 가능성을 생각해 볼 수 있습니다.
#
# 마지막으로 실행 결과를 바탕으로 하루 중 평균 대여량이 높은 시간대,
# 기온과 대여량의 관계, MAE와 RMSE가 의미하는 실제 예측 오차,
# R²가 나타내는 모델의 설명력을 정리하세요.
# 잔차 그래프에 일정한 패턴이 있는지도 확인하고,
# 현재의 다중선형회귀 모델이 서울 공공자전거 수요를 분석하는 데
# 어떤 장점과 한계를 가지는지 간단히 정리하세요.