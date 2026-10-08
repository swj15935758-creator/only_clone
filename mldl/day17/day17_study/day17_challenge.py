# day17_challenge.py
# 주제:Day 17 Challenge 과제
# 주제: 주택가격 단순회귀와 다중회귀 비교
#
# 아래 특성을 이용하여 주택가격을 예측하려고 한다.
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from include.graph_config import set_graph
from python.print_util import pp
# 면적(㎡): [45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140]
# 역거리(분): [18, 15, 14, 16, 12, 13, 10, 11, 9, 8, 10, 7, 6, 8, 5, 6, 4, 5, 3, 4]
# 준공연수(년): [24, 20, 18, 22, 15, 17, 14, 12, 13, 10, 11, 9, 8, 10, 7, 6, 5, 7, 4, 3]
# 가격(만원): [33300, 37000, 41200, 40300, 46650, 46950, 52100, 53100, 56450, 60000, 59650, 64550, 66800, 68200, 71250, 73900, 76450, 78250, 81300, 83550]

df = pd.DataFrame({
    '면적(㎡)': [45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140],
    '역거리(분)': [18, 15, 14, 16, 12, 13, 10, 11, 9, 8, 10, 7, 6, 8, 5, 6, 4, 5, 3, 4],
    '준공연수(년)': [24, 20, 18, 22, 15, 17, 14, 12, 13, 10, 11, 9, 8, 10, 7, 6, 5, 7, 4, 3],
    '가격(만원)': [33300, 37000, 41200, 40300, 46650, 46950, 52100, 53100, 56450, 60000, 59650, 64550, 66800, 68200, 71250, 73900, 76450, 78250, 81300, 83550],
})
# 요구사항
# 두 모델 모두 테스트 비율 25%, random_state=42를 사용한다.
# 단순회귀 모델은 면적만 사용한다. 면적(㎡)
RANDOM_SEED = 42
X = df[['면적(㎡)']]
y = df['가격(만원)']
easy_X_train, easy_X_test, easy_y_train, easy_y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=RANDOM_SEED,
    shuffle=True
)
easy_model = LinearRegression()
easy_model.fit(easy_X_train, easy_y_train)
easy_pred = easy_model.predict(easy_X_test)
# pp(easy_pred)

# 다중회귀 모델은 면적, 역거리, 준공연수를 사용한다.
multi_X = df[['면적(㎡)','역거리(분)','준공연수(년)']]
milti_y = df['가격(만원)']
multi_X_train, multi_X_test, multi_y_train, multi_y_test = train_test_split(
    multi_X,
    milti_y,
    test_size=0.25,
    random_state=RANDOM_SEED,
    shuffle=True
)
multi_model = LinearRegression()
multi_model.fit(multi_X_train, multi_y_train)
multi_pred = multi_model.predict(multi_X_test)
# pp(multi_pred)

# 두 모델의 MAE와 R²를 계산하여 비교 DataFrame으로 출력한다.
easy_mae = mean_absolute_error(easy_y_test, easy_pred)
easy_r2_score = r2_score(easy_y_test, easy_pred)

multi_mae = mean_absolute_error(multi_y_test, multi_pred)
multi_r2_score = r2_score(multi_y_test, multi_pred)

comparison = pd.DataFrame({
    '모델': ['단순선형회귀', '다중선형회귀'],
    'MAE': [easy_mae, multi_mae],
    'R^2': [easy_r2_score, multi_r2_score]
})
pp(comparison)
# 면적 100㎡, 역거리 5분, 준공연수 6년인 주택의 예상 가격을 다중회귀 모델로 예측한다.
new_X = pd.DataFrame({
    '면적(㎡)': [100],
    '역거리(분)' :[5],
    '준공연수(년)':[6]
})

# 다중회귀 모델의 특성별 회귀계수를 DataFrame으로 출력한다.
coefficient_df = pd.DataFrame({
    '특성': multi_X.columns,
    '회귀계수': multi_model.coef_
})
pp(coefficient_df)

new_pred_y = multi_model.predict(new_X) #[66256.18645418]
pp(new_pred_y)


# 단순회귀의 면적-가격 산점도와 회귀선을 작성한다.
set_graph(10, 8, 13)
line_x = pd.DataFrame({
    '면적(㎡)': sorted(df['면적(㎡)'])
})
line_y = easy_model.predict(line_x)
plt.scatter(df['면적(㎡)'], df['가격(만원)'])
plt.plot(line_x['면적(㎡)'], line_y)
plt.xlabel('면적(㎡)')
plt.ylabel('가격(만원)')
plt.title('단순 선형회귀')
plt.show()

# 두 모델 중 테스트 데이터 기준으로 더 적절한 모델을 MAE와 R²를 근거로 코드 마지막에 문자열로 출력한다.
pp('MAE는 예측 가격이 실제 가격과 평균적으로 얼마나 차이 나는지를 의미해서 숫자가 작을수록 좋다. '
   'R²는 모델이 실제 가격의 변화를 얼마나 잘 설명하는지를 나타내기 때문에 1에 가까울수록 좋다.')
pp('다중선형회귀 모델이 단순선형회귀 모델보다 MAE가 작고 R²가 1에 더 가까우므로 '
   '테스트 데이터 기준으로 다중선형회귀 모델이 더 적절하다.')
# 계수의 절댓값만으로 특성 중요도를 단정하면 안 되는 이유를 주석으로 작성한다.
# 특성마다 단위와 값의 크기가 다르기 때문에 계수의 절댓값만으로 특성 중요도를 단정하면 안 된다.

