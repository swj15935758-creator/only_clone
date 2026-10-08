# extra.py

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from include.graph_config import set_graph
from python.print_util import pp


set_graph(8,5,13)
DATA_FILE = Path(__file__).resolve().parent / "assets" / 'SeoulBikeData_ko.csv'
# pp(DATA_FILE) # 파일경로

# 데이터 프레임 생성
df = pd.read_csv(DATA_FILE,encoding='utf-8-sig')
pp(df.shape) #(8760, 14)
pp(df.head())
pp(df.dtypes)
pp(df.isna().sum())
pp(df.duplicated().sum())

# 날짜 문자열을 datetime 타입으로 변환
# dayfirst=True : 01/12/2017 을 17년 12월 1일로 해석하도록 지정
df['날짜'] = pd.to_datetime(df['날짜'],dayfirst=True)
df['월'] = df['날짜'].dt.month
df['요일'] = df['날짜'].dt.dayofweek

# 운영여부가 Yes 인 행 춫ㄹ해서 데이터 프레임 복제
df = df[df['운영여부']=='Yes'].copy()
pp(df.shape)

# 시간별 평균 대여량 계산/ 출력
hourly_mean = df.groupby('시간')['대여량'].mean()
pp(hourly_mean.round(1))

# # 시간대별 평균 데여량 선 그래프
# plt.plot(hourly_mean.index,hourly_mean.values,marker='o')
# plt.title('시간대별 평균 공공 자전거 대여량')
# plt.xlabel('시간')
# plt.ylabel('평균데여량')
# plt.xticks(range(24))# x 축에 0부터 23 tick 생성
# plt.tight_layout()
# plt.show()
#
# # 기온과 대여량의 관계를 확인하기 위한 산점도 그래프
# plt.scatter(df['기온'],df['대여량'],alpha=0.5,s=12)
# plt.title('기온과 공공 자전거 대여량')
# plt.xlabel('온도(C)')
# plt.ylabel('대여량')
# plt.tight_layout()
# plt.show()

# 다중회귀에 사용할 수치형 독립변수 목록
numeric_features = ['시간','기온','습도','풍속','가시거리','일사량','강수량','적설량','월','요일']

# 문자열로 구성된 범주형 독립 변수 목록
categorical_features = ['계절','휴일']

# 선택한 수치형 변수와 범주형 변수로 독립변수 X 구성
X = df[numeric_features + categorical_features].copy()

# 범주형 데이터를 선형회귀 모델이 처리할 수 있도록 0과 1의 더미 변수로 변환
# 모델이 처리할 수 있도록 0과 1로 수치화 시킴
# drop_first = True : 기준 범주 하나를 제외 해서 불필요한 중복 변수를 줄임
X = pd.get_dummies(
    X, # 원본 데이터 프레임
    columns=categorical_features, # 범주형 변수
    drop_first=True,
    dtype = int
)
pp(X)


y = df['대여량'] # 예측 대상인 시간당 자전거 대여량을 종속 변수 y로 지정

# 실제 모델에 사용되는 독립변수 이름을 확인
pp(X.columns.tolist())
pp(X.shape,y.shape) # (8465, 14) (8465,)

# 학습 / 테스트 분리
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

pp(X_train.shape,X_test.shape,y_train.shape,y_test.shape)

# 다중 선형 회귀 모델 객체를 생성
model = LinearRegression()
# 모델의 회귀계수와 절편을 학습시켜서 만듬
model.fit(X_train,y_train)
# 테스트 데이터에 대한 자전거 대여량을 예측
y_pred = model.predict(X_test)

# 선형회귀는 대여량이 0 이상이어야 한다는 제약을 자동으로
# 적용하지 않으므로 예측 범위를 확인
pp(f'최소:{y_pred.min():.2f}')
pp(f'최대:{y_pred.max():.2f}')


# MAE
mae = mean_absolute_error(y_test,y_pred)

# MSE
mse = mean_squared_error(y_test,y_pred)

# RMSE
rmse = np.sqrt(mean_squared_error(y_test,y_pred))

# R^2
r2 = r2_score(y_test,y_pred)

# 평가 지표 출력
pp(f'MAE:{mae:.2f}')
pp(f'MSE:{mse:.2f}')
pp(f'RMSE:{rmse:.2f}')
pp(f'R^2:{r2:.2f}')

# 실제 값과 예측값을 비교하기 위한 DataFrame 생성
result = pd.DataFrame({
    '실제대여량' : y_test.to_numpy(),
    '예측대여량' : y_pred,
})
pp(result)

# 잔차
result['오차'] = result['실제대여량'] - result['예측대여량']

# 오차의 크기만 확인하기 위한 절대값을 계산
result['절대오차'] = result['오차'].abs()
pp(result)

# 절편 출력
pp(f'{model.intercept_:.4f}')

# 독립변수 별로 회귀 계수를 DataFrame 으로 정리
coef_df = pd.DataFrame({
    '특성' : X.columns,
    '회귀계수' : model.coef_,
})
pp(coef_df)

# 회귀계수 양수와 음수를 쉽게 확인 할 수 있도록 방향 컬럼을 생성
coef_df['방향'] = np.where(coef_df['회귀계수'] >=0,'양수','음수')
pp(coef_df)

# 실제 값과 예측값 관계를 확인하기 위한 산점도 그래프
plt.scatter(y_test, y_pred,alpha=0.5,s=15)
# 실제값과 예측값 중에 더 가장 작은 값, 기준선 시작점
min_value = min(y_test.min(),y_pred.min())
# 실제값과 예측값 중에 더 가장 큰 값, 기준선 끝점
max_value = max(y_test.max(),y_pred.max())

# # 기준선 그래프
# plt.plot(
#     [min_value,max_value],
#     [min_value,max_value],
#     linestyle = '--',
#     label = '완벽한 예측(y=X)'
# )
# plt.title('실제 대여량과 실제 대여량')
# plt.xlabel('실제 대여량')
# plt.ylabel('실제 예츨량')
# plt.legend()
# plt.tight_layout()
# plt.show()

# 잔차를 넘파이 배열로 계산
residuals = y_test.to_numpy() - y_pred

# # 예측 대여량에 따른 잔차의 분포 산점도 그래프
# plt.scatter(y_pred,residuals,alpha=0.3,s=15)
# plt.axhline(0,linestyle='--') # 잔차가 0 인위치를 찾기 위한 수평선
# plt.title('다중회귀 잔차 분석')
# plt.xlabel('예측 대여량')
# plt.ylabel('잔차')
# plt.tight_layout()
# plt.show()

# 분석에 사용한 주요 수치 변수와 대여량의 상관 계수를 계산
corr_columns = numeric_features + ['대여량']

# 대여량과 각 수치 변수의 상관 계수만 선택
correlation = df[corr_columns].corr(numeric_only=True)['대여량'].drop('대여량')

# 상관계수 절대값이 큰 변수 부터 확인할 수 있도록 정렬
correlation = correlation.reindex( # 인덱스 재구성
    correlation.abs().sort_values(ascending=False).index,
)

# 수치형 변수와 대여량의 상관관계를 출력
pp(correlation.round(4))

# 분석 결과 핵심 수치를 출력
pp(f'MAE 가 {mae:.2f}이므로 예측 대여량은 실제 대여량과 평균 약{mae:.0f}대 차이가남')
pp(f'RMSE가 {rmse:.2f}이므로 큰 예측 오차까지 반영하면 대표적인 오차 크기는 약{rmse:.2f}')
pp(f'R^2가 {r2:.4f}이므로 모델은 데티스 데이터 데여량 변동의 약{r2 * 100:.1f}%를 설명')
pp(f'잔차 그레프에 곡선이나 시간대별 패턴이 남는다면 선형 회귀가 비선형 적인 수요 패턴을 충분히 설명하지 못한거다')