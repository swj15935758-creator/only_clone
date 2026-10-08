# day18_basic.py
# 주제:AI휴먼 day18 Basic 과제
# 주제: 붓꽃 품종 분류
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
from sklearn.datasets import load_iris

# 목표
# scikit-learn의 Iris 데이터를 사용하여 Logistic Regression으로 3개 붓꽃 품종을 분류합니다.
# https://scikit-learn.org/stable/datasets/toy_dataset.html
#
# 요구사항

# load_iris(as_frame=True)로 Iris 데이터를 불러옵니다.
iris = load_iris(as_frame=True)
# 입력 특성은 4개 특성을 모두 사용합니다.
X = iris.data
# 정답은 target 컬럼을 사용합니다.
y = iris.target
# 학습 데이터 80%, 테스트 데이터 20%로 분리합니다.
X_train,X_test,y_train,y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
# random_state=42, stratify=y를 적용합니다.
# LogisticRegression(max_iter=1000) 모델을 학습합니다.
logistic = LogisticRegression(
    max_iter=1000,
    C=1.0,
    solver='lbfgs',
    random_state=42,
)
logistic.fit(X_train, y_train) # 학습

# 테스트 데이터의 예측 클래스를 구합니다.
pp(logistic.classes_) # [0 1 2]
pp(logistic.intercept_) # [0 1 2]
# 정확도를 계산하여 출력합니다.
pp(logistic.score(X_test, y_test)) # 0.9666666666666667

# 테스트 데이터 앞 5건에 대해 실제값과 예측값을 DataFrame으로 만들어 출력합니다.
logistic_pred = logistic.predict(X_test)

iris_frame = pd.DataFrame({
    '실제값': y_test.head(5).to_numpy(),
    '예측값' : logistic_pred[:5],
})

pp(iris_frame)
# 테스트 데이터 앞 3건에 대해 클래스별 예측 확률을 출력합니다.
# 테스트 데이터 앞 3건에 대해 클래스별 예측 확률을 출력합니다.
proba = logistic.predict_proba(X_test.head(3))

proba_df = pd.DataFrame(
    proba,
    columns=iris.target_names
)

pp(proba_df)

# 컬럼명
# sepal length (cm)    꽃받침 길이(cm)
# sepal width (cm)    꽃받침 너비(cm)
# petal length (cm)    꽃잎 길이(cm)
# petal width (cm)    꽃잎 너비(cm)
# target    품종
