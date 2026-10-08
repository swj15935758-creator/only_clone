# day17_application.py
# 주제:Day 17 Application 과제
# 주제: 온라인 광고비로 매출 예측 및 MAE 평가
#
# 아래 데이터는 온라인 광고비와 월 매출 데이터이다.
#
# 광고비(만원): [80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380]
# 매출(만원): [1050, 1120, 1220, 1280, 1380, 1490, 1580, 1660, 1770, 1850, 1960, 2070, 2160, 2260, 2370, 2460]
#


import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from include.graph_config import set_graph
from python.print_util import pp

set_graph(10, 8, 13)

# 요구사항
# pandas DataFrame으로 데이터를 구성한다.
df = pd.DataFrame({
    '광고비': [80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380],
    '매출': [1050, 1120, 1220, 1280, 1380, 1490, 1580, 1660, 1770, 1850, 1960, 2070, 2160, 2260, 2370, 2460]
})

# 광고비를 X, 매출을 y로 정의한다.
X = df[['광고비']]
y = df['매출']

# 전체 데이터의 25%를 테스트 데이터로 분리하고 random_state=42를 사용한다.
RANDOM_SEED = 42

# LinearRegression 모델을 학습하고 테스트 데이터의 매출을 예측한다.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=RANDOM_SEED,
    shuffle=True
)

model = LinearRegression()
model.fit(X_train, y_train)

pred = model.predict(X_test)

# 실제매출, 예측매출, 절대오차를 하나의 DataFrame으로 작성한다.
new_df = pd.DataFrame({
    '실제매출': y_test,
    '예측매출': pred
})

new_df['절대오차'] = abs(new_df['실제매출'] - new_df['예측매출'])

pp(new_df)
# MAE를 계산해 출력한다.
mae = mean_absolute_error(y_test, pred)
pp(mae) # 25.77617328519858
# R²를 추가로 계산해 출력한다.
r2 = r2_score(y_test, pred)
pp(r2)
# 광고비가 400만원일 때 예상 매출을 예측한다.
test_X = pd.DataFrame({
    '광고비' : [400]
})
pred_test_X = model.predict(test_X)
pp(pred_test_X) #[2545.78519856]
# 산점도와 회귀선을 한 그래프에 표시한다.
plt.scatter(df['광고비'], df['매출'])

# 회귀선 산점도 그래프
line_x = pd.DataFrame({
    '광고비': sorted(df['광고비'])
})
line_y = model.predict(line_x)
plt.plot(line_x['광고비'], line_y)
plt.xlabel('광고비')
plt.ylabel('매출')
plt.title('회귀선 산점도')
plt.show()

# MAE가 실무적으로 무엇을 의미하는지 코드 주석으로 1줄 설명한다
# MAE는 예측 매출이 실제 매출과 평균적으로 얼마나 차이 나는지를 의미한다.