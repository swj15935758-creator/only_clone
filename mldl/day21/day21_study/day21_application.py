# day21_application.py
# 주제:구독 서비스 고객 이탈 모델의 안정적인 교차검증
#
# 상황
# 구독 서비스 회사가 고객 이탈 여부를 예측하려고 합니다.
# 한 번의 Train/Test 분할 결과만으로 모델을 판단하지 않고 Pipeline과 Stratified 5-Fold Cross Validation을 사용해 안정적으로 평가하려고 합니다.
#
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
from sklearn.metrics import accuracy_score, f1_score
# 데이터 분할·교차검증·하이퍼파라미터 탐색 기능 사용
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, GridSearchCV,cross_validate
# 요구사항
# make_classification()으로 1,000건, 특성 8개의 이진 분류 데이터를 생성합니다.
# 고객 이탈 가상 데이터 생성
# weights=[0.7, 0.3], class_sep=1.0, random_state=20을 사용합니다.
X_array, y = make_classification(
    n_samples=1000,       # 고객 수
    n_features=8,         # 고객 행동/거래 특성 수
    n_informative=6,      # 실제 분류에 정보를 주는 특성 수
    n_redundant=1,        # 다른 특성 조합으로 표현되는 중복 특성 수
    weights=[0.7, 0.3],   # 유지 70%, 이탈 30%의 불균형을 가정
    class_sep=1.0,
    random_state=20
)
# 특성 컬럼명은 이용기간, 월사용량, 문의횟수, 평균결제액, 할인율, 접속일수, 콘텐츠수, 만족도처럼 업무 의미가 드러나게 구성합니다.
columns = ["이용기간", "월사용량", "문의횟수", "평균결제액", "할인율", "접속일수", "콘텐츠수", "만족도"]
X = pd.DataFrame(X_array, columns=columns)
X["평균결제액"] = X["평균결제액"] * 50000 + 80000  # 원 단위 결제액처럼 큰 스케일을 구성
X["할인율"] = X["할인율"] * 0.05 + 0.1            # 비율 데이터처럼 작은 스케일을 구성
pp("데이터 크기", X.shape)
pp("이탈 비율", pd.Series(y).value_counts(normalize=True).sort_index().round(3))

# StandardScaler와 LogisticRegression(max_iter=3000)을 Pipeline으로 연결합니다.
pipe = Pipeline(steps=[
    ('scaler', StandardScaler()),
    ('model', LogisticRegression(max_iter=3000))
])
# StratifiedKFold(n_splits=5, shuffle=True, random_state=20)을 사용합니다.
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=20
)
# cross_val_score()로 accuracy와 f1을 각각 계산합니다.
acc_scores = cross_val_score(
    pipe,
    X,
    y,
    cv=cv, # 폴드 5개
    scoring='accuracy',
    n_jobs=-1
)
f1_scores = cross_val_score(
    pipe,
    X,
    y,
    cv=cv, # 폴드 5개
    scoring='f1',
    n_jobs=-1
)
# Fold별 점수
pp('Accuracy Fold별 점수:', np.round(acc_scores, 4))
pp('F1 Fold별 점수:', np.round(f1_scores, 4))

# 평균과 표준편차
pp('Accuracy 평균:', round(acc_scores.mean(), 4))
pp('Accuracy 표준편차:', round(acc_scores.std(), 4))

pp('F1 평균:', round(f1_scores.mean(), 4))
pp('F1 표준편차:', round(f1_scores.std(), 4))
# cross_validate()로 train_accuracy와 validation_accuracy를 구해 평균 Gap을 계산합니다.
cv_results = cross_validate(
    pipe,
    X,
    y,
    cv=cv,
    scoring='accuracy',
    return_train_score=True,
    n_jobs=-1
)

# Fold별 Train Accuracy
train_acc_scores = cv_results['train_score']

# Fold별 Validation Accuracy
validation_acc_scores = cv_results['test_score']
pp('Train Accuracy Fold별 점수:',np.round(train_acc_scores, 4))
pp('Validation Accuracy Fold별 점수:',np.round(validation_acc_scores, 4))

# Train Accuracy 평균
train_acc_mean = train_acc_scores.mean()

# Validation Accuracy 평균
validation_acc_mean = validation_acc_scores.mean()

# Train - Validation 평균 차이
accuracy_gap = train_acc_mean - validation_acc_mean

pp('Train Accuracy 평균:',round(train_acc_mean, 4))

pp('Validation Accuracy 평균:',round(validation_acc_mean, 4))

pp('Train/Validation Accuracy Gap:',round(accuracy_gap, 4))
# Hold-out 방식으로도 Train 80%, Test 20%를 나누어 Test Accuracy와 F1을 구합니다.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=20
)
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
holdout_accuracy = accuracy_score(
    y_test,
    y_pred
)

holdout_f1 = f1_score(
    y_test,
    y_pred
)

pp('Hold-out Accuracy:',round(holdout_accuracy, 4))

pp('Hold-out F1:',round(holdout_f1, 4))

# Hold-out 점수와 CV 평균을 비교하고, 둘이 다른 이유를 3문장 이내로 정리합니다.
pp('CV Accuracy 평균:',round(acc_scores.mean(), 4))

pp('Hold-out Accuracy:',round(holdout_accuracy, 4))

pp('CV F1 평균:',round(f1_scores.mean(), 4))

pp('Hold-out F1:',round(holdout_f1, 4))

print("CV는 전체 데이터를 여러 Fold로 나누어 반복 평가한 평균 성능입니다.")
print("Hold-out은 한 번 나눈 Test 데이터로 평가하기 때문에 데이터 분할에 따라 CV 평균과 점수가 다를 수 있습니다.")
print("따라서 CV는 한 번의 Hold-out 결과보다 모델의 전반적인 성능과 안정성을 확인하는 데 도움이 됩니다.")

# Fold별 F1 점수를 선그래프로 시각화합니다.
set_graph()

fold_numbers = range(1, 6)

plt.plot(
    fold_numbers,
    f1_scores,
    marker='o'
)

plt.title('Fold별 F1 Score')
plt.xlabel('Fold')
plt.ylabel('F1 Score')
plt.xticks(fold_numbers)
plt.grid(True)
plt.show()


#
# 제출 결과
# 5-Fold Accuracy/F1 점수 배열
# 각 지표 평균과 표준편차
# Train/Validation Accuracy Gap
# Hold-out Accuracy/F1
# Fold별 F1 그래프
# 평가 결과 해석