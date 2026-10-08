# day17_basic.py
# 주제:Day 17 Basic 과제
# 주제: 공부시간으로 평가점수 예측
#
# 아래 데이터를 이용하여 공부시간에 따른 평가점수를 예측하는 단순 선형회귀 모델을 작성하시오.
#
# 공부시간: [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5]
# 평가점수: [48, 52, 55, 60, 63, 68, 72, 75, 80, 83, 87, 91]
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
    '공부시간': [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5],
    '평가점수': [48, 52, 55, 60, 63, 68, 72, 75, 80, 83, 87, 91]
})
# 공부시간을 X, 평가점수를 y로 정의한다.
X = df[['공부시간']]
y = df['평가점수']

RANDOM_SEED = 42
# train, test 분리
# 전체 데이터의 25%를 테스트 데이터로 사용한다.
# random_state=42를 사용한다.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=RANDOM_SEED,
    shuffle=True
)

# LinearRegression 모델을 학습한다.
model = LinearRegression()
model.fit(X_train, y_train)
pred = model.predict(X_test)
# 테스트 데이터의 실제점수와 예측점수를 DataFrame으로 출력한다.
pp('실제점수: ',y_test)
pp('예측점수: ',pred)
# 7시간 공부했을 때의 예상 평가점수를 출력한다.
new_X = pd.DataFrame({
    '공부시간' : [7]
})
new_pred = model.predict(new_X)
pp(new_pred)
# 공부시간과 평가점수의 산점도 및 회귀선을 그린다.
plt.scatter(df['공부시간'],df['평가점수'])
line_X = pd.DataFrame({'공부시간' : sorted(df['공부시간'])})
line_y = model.predict(line_X)
plt.plot(line_X,line_y)
plt.xlabel('공부시간')
plt.ylabel('평가점수')
plt.title('단순회귀 산점도')
plt.show()



