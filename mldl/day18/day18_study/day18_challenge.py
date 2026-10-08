# day18_challenge.py
# 주제:AI휴먼 day18 Challenge 과제
# 주제: 손글씨 숫자 0~9 분류 모델 비교
import sklearn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import to_numeric
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from include.graph_config import set_graph
from python.print_util import pp
from sklearn.datasets import load_digits
# 목표
# Digits 데이터를 사용하여 Logistic Regression과 KNN의 다중 분류 성능을 비교하고 오분류 사례를 분석합니다.
# https://scikit-learn.org/stable/datasets/toy_dataset.html
set_graph(10,8,12)
# 요구사항
#
# load_digits(as_frame=True)로 손글씨 숫자 데이터를 불러옵니다.
df_digits = load_digits(as_frame=True)
# 입력은 data.data, 정답은 data.target을 사용합니다.
X=df_digits.data
y=df_digits.target
# 학습 데이터 75%, 테스트 데이터 25%로 분리합니다.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
# random_state=42, stratify=y를 적용합니다.
    random_state=42,
    stratify=y,
)
# 다음 두 모델을 학습합니다.
# LogisticRegression(max_iter=3000)
logistic_digit = LogisticRegression(
    max_iter=3000,
    C=1.0,
    solver='lbfgs',
    random_state=42,
)
logistic_digit.fit(X_train, y_train) # 학습
# KNeighborsClassifier(n_neighbors=3)
knn_digits = KNeighborsClassifier(
    n_neighbors=3, # 참고할 가장 가까운 이웃의 (K)수
    weights='uniform', # 각이웃의 가중치 동일하게 적용
    metric='minkowski', # 거리 계산 알고리즘
    p=2 # Euclidean Distance : 두점 사이의 거리 (직선거리)
)
knn_digits.fit(X_train, y_train) # 학습

# 각 모델의 정확도를 계산합니다.
acc_logistic = logistic_digit.score(X_test, y_test) # 로직 정확도
acc_knn = knn_digits.score(X_test, y_test) # knn 정확도 이게 높음

# 모델, 정확도, 정답수, 오답수 컬럼을 가진 비교표를 만듭니다.
logistic_pred = logistic_digit.predict(X_test)
logistic_correct = (y_test == logistic_pred).sum() # 정답수
logistic_wrong = (y_test != logistic_pred).sum() # 오답수


knn_pred = knn_digits.predict(X_test)
knn_correct = (y_test == knn_pred).sum() # 정답수
knn_wrong = (y_test != knn_pred).sum() # 오답수

comparison = pd.DataFrame({
    '모델': ['logistic', 'knn'],
    '정확도': [acc_logistic, acc_knn],
    '정답수': [logistic_correct, knn_correct],
    '오답수': [logistic_wrong, knn_wrong]
})

pp(comparison)

# 정확도가 높은 모델 이름을 출력합니다.
best_index = comparison['정확도'].idxmax()
pp(comparison.loc[best_index])

# 정확도가 높은 모델의 오분류 데이터를 찾아 앞 10건의 실제값과 예측값을 출력합니다.
result = X_test.copy()
result['정답'] = y_test
result['예측'] = knn_digits.predict(X_test)
wrong = result['정답'] != result['예측'] # 불리언 시리즈

# 오분류 데이터만 가져오기
wrong_result = result[wrong]

# 오분류 데이터 앞 10건의 실제값과 예측값 출력
pp(wrong_result[['정답','예측']].head(10))

# 오분류 개수
count_wrong = wrong.sum()
pp(count_wrong)

# 실제 숫자별로 오분류가 몇 건 발생했는지 집계하여 출력합니다.
wrong_count = wrong_result['정답'].value_counts().sort_index()
pp(wrong_count)

# 두 모델의 정확도를 막대그래프로 비교합니다.
plt.bar(comparison['모델'],comparison['정확도'])
plt.xlabel('모델')
plt.ylabel('정확도')
plt.title('모델별 정확도 비교')
plt.show()
# data
#
# data.data        8×8 이미지의 64개 픽셀 밝기값
# data.target    손글씨 숫자(0~9)
