# day21_challenge.py
# 주제: 대출 연체 위험 예측 모델의 Pipeline + GridSearchCV 튜닝
# 상황
# 금융 서비스에서 대출 연체 위험 고객을 탐지하려고 합니다.
# 연체 고객 비율이 낮기 때문에 Accuracy만 최대화하지 않고 F1을 기준으로 KNN 모델의 하이퍼파라미터를 탐색합니다.
from sklearn.neighbors import KNeighborsClassifier

from print_util import pp
from include.graph_config import set_graph
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler # 특성별 평균 0·표준편차 1 수준으로 표준화
from sklearn.linear_model import LogisticRegression # 클래스 확률을 학습하는 로지스틱 회귀 분류 모델 사용
from sklearn.pipeline import Pipeline, make_pipeline # 전처리와 모델 학습 단계를 하나의 흐름으로 연결
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
# 데이터 분할·교차검증·하이퍼파라미터 탐색 기능 사용
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, GridSearchCV,cross_validate

# 연체 위험 가상 데이터 생성
X_array, y = make_classification(
    n_samples=1500,
    n_features=10,
    n_informative=7,
    n_redundant=1,
    weights=[0.82, 0.18],  # 정상 82%, 연체 18%의 불균형을 가정
    class_sep=0.9,
    flip_y=0.02,          # 실제 데이터의 라벨 오류/잡음을 일부 반영
    random_state=20
)
columns = ["연소득", "부채비율", "신용기간", "최근연체수", "카드사용률", "대출건수", "월상환액", "거래기간", "계좌잔액", "신용조회수"]
X = pd.DataFrame(X_array, columns=columns)
X["연소득"] = X["연소득"] * 20000000 + 50000000
X["월상환액"] = X["월상환액"] * 500000 + 1500000
X["계좌잔액"] = X["계좌잔액"] * 10000000 + 20000000
pp("데이터 크기", X.shape)
pp("클래스 비율", pd.Series(y).value_counts(normalize=True).sort_index().round(3))
pp("특성별 표준편차", X.std().round(2))

# - Train 80%, Test 20%로 분할하고 stratify=y를 적용합니다.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=20
)
# - Pipeline 단계 이름은 scaler, model을 사용합니다
# - model은 KNeighborsClassifier()를 사용합니다.
pipe = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("model", KNeighborsClassifier()),
])
# - StratifiedKFold 5-Fold를 사용합니다.
cv = StratifiedKFold(
    n_splits=5, # 폴드 5개
    shuffle=True, # 분할 전에 샘플을 무작위로 섞음
    random_state=20
)

# - 아래 하이퍼파라미터를 탐색합니다.
param_grid = {
    "model__n_neighbors": [3, 5, 7, 9, 13],
    "model__weights": ["uniform", "distance"],
    "model__p": [1, 2]
}

# - GridSearchCV의 scoring은 f1로 지정합니다.
# - n_jobs=-1, return_train_score=True를 사용합니다.
grid = GridSearchCV(
    estimator=pipe,
    param_grid=param_grid,
    scoring="f1",
    cv=cv,
    n_jobs=-1,
    return_train_score=True
)

# Train 데이터로 모든 하이퍼파라미터 조합을 학습하고 평가합니다.
grid.fit(X_train, y_train)

# - best_params_, best_score_를 출력합니다.
pp("최적 파라미터", grid.best_params_)
pp("최적 CV F1", round(grid.best_score_, 4))

# - cv_results_를 DataFrame으로 변환해 rank_test_score 상위 10개 조합을 출력합니다.
cv_result_df = pd.DataFrame(grid.cv_results_)

top10 = cv_result_df.sort_values(
    by="rank_test_score"
).head(10)

top10 = top10[[
    "rank_test_score",
    "param_model__n_neighbors",
    "param_model__weights",
    "param_model__p",
    "mean_train_score",
    "mean_test_score",
    "std_test_score"
]]

pp("상위 10개 탐색 결과표", top10)

# - 최적 모델로 Test Accuracy, Precision, Recall, F1을 계산합니다.
best_model = grid.best_estimator_

y_pred = best_model.predict(X_test)

test_accuracy = accuracy_score(
    y_test,
    y_pred
)

test_precision = precision_score(
    y_test,
    y_pred
)

test_recall = recall_score(
    y_test,
    y_pred
)

test_f1 = f1_score(
    y_test,
    y_pred
)

pp("최적 모델 Test Accuracy", round(test_accuracy, 4))
pp("최적 모델 Test Precision", round(test_precision, 4))
pp("최적 모델 Test Recall", round(test_recall, 4))
pp("최적 모델 Test F1", round(test_f1, 4))

# - Confusion Matrix를 출력합니다.
conf_matrix = confusion_matrix(
    y_test,
    y_pred
)

pp("Confusion Matrix", conf_matrix)

# - 기본 KNN(n_neighbors=5) Pipeline과 최적 모델의 Test F1을 비교합니다.
basic_pipe = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("model", KNeighborsClassifier(n_neighbors=5)),
])

basic_pipe.fit(X_train, y_train)

basic_y_pred = basic_pipe.predict(X_test)

basic_f1 = f1_score(
    y_test,
    basic_y_pred
)

pp("기본 KNN Test F1", round(basic_f1, 4))
pp("최적 모델 Test F1", round(test_f1, 4))
pp("Test F1 차이", round(test_f1 - basic_f1, 4))

# - n_neighbors별 평균 CV F1을 weights 기준으로 선그래프로 시각화합니다. p=2 결과만 사용합니다.
p2_result = cv_result_df[
    cv_result_df["param_model__p"] == 2
]

uniform_result = p2_result[
    p2_result["param_model__weights"] == "uniform"
].sort_values(
    by="param_model__n_neighbors"
)

distance_result = p2_result[
    p2_result["param_model__weights"] == "distance"
].sort_values(
    by="param_model__n_neighbors"
)

set_graph()

plt.plot(
    uniform_result["param_model__n_neighbors"],
    uniform_result["mean_test_score"],
    marker="o",
    label="uniform"
)

plt.plot(
    distance_result["param_model__n_neighbors"],
    distance_result["mean_test_score"],
    marker="o",
    label="distance"
)

plt.title("n_neighbors별 평균 CV F1")
plt.xlabel("n_neighbors")
plt.ylabel("평균 CV F1")
plt.legend()
plt.grid(True)
plt.show()

# - 최적 모델의 Recall이 충분하지 않다고 판단되는 경우 무엇을 추가로 검토해야 하는지 3가지 이상 정리합니다.
print("Recall 개선을 위한 추가 검토 항목")
print("1. 연체 고객을 더 많이 탐지하도록 예측 확률의 분류 기준값을 조정할 수 있습니다.")
print("2. 불균형 데이터 문제를 완화하기 위해 Over Sampling 또는 Under Sampling을 검토할 수 있습니다.")
print("3. GridSearchCV의 평가 기준을 Recall 또는 F-beta Score 등으로 변경하여 탐색할 수 있습니다.")
print("4. 연체 위험을 설명하는 새로운 특성을 추가하거나 기존 특성을 개선할 수 있습니다.")
print("5. KNN 외에 다른 분류 모델도 함께 비교할 수 있습니다.")


#
# 제출 결과
# 최적 파라미터
# 최적 CV F1
# 상위 10개 탐색 결과표
# 기본 모델과 최적 모델의 Test F1 비교
# Accuracy, Precision, Recall, F1
# Confusion Matrix
# 튜닝 결과 그래프
# Recall 개선을 위한 추가 검토 항목