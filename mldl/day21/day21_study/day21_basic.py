# day21_basic.py
# 주제:제조 설비 센서 데이터의 Scaling 효과 비교
#
# 상황
# 제조 설비에서 수집한 센서 데이터로 정상/이상 상태를 분류하려고 합니다.
# 센서마다 단위가 달라 값의 범위 차이가 매우 큽니다.
# KNN 모델을 사용하여 StandardScaler 적용 전후의 성능을 비교하십시오.
from sklearn.neighbors import KNeighborsClassifier

from print_util import pp
from include.graph_config import set_graph
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler # 특성별 평균 0·표준편차 1 수준으로 표준화
from sklearn.linear_model import LogisticRegression # 클래스 확률을 학습하는 로지스틱 회귀 분류 모델 사용
from sklearn.pipeline import Pipeline, make_pipeline # 전처리와 모델 학습 단계를 하나의 흐름으로 연결
# 데이터 분할·교차검증·하이퍼파라미터 탐색 기능 사용
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, GridSearchCV

# 요구사항
# sklearn.datasets.make_classification()으로 600건의 이진 분류 데이터를 생성합니다.
X_array, y = make_classification(
    n_samples=600,       # 전체 데이터 600건
    n_features=5,        # 특성 5개
    n_informative=4,     # 실제 분류에 도움이 되는 특성 4개
    n_redundant=0,       # 중복 특성 없음
    class_sep=1.2,       # 클래스 분리 정도
    random_state=20
)
# 특성은 5개로 구성하고 random_state=20을 사용합니다.
# 생성된 특성 중 두 개 컬럼에 각각 1000, 0.01을 곱해 인위적으로 스케일 차이를 만듭니다.
X = pd.DataFrame(
    X_array,
    columns=["진동", "온도", "압력", "전류", "소음"]
)

# 3. 인위적으로 센서별 스케일 차이 만들기
X["진동"] = X["진동"] * 1000
X["소음"] = X["소음"] * 0.01

pp("특성별 표준편차", X.std().round(3))

# train_test_split()으로 Train 75%, Test 25%로 분할합니다.
# stratify=y, random_state=20을 적용합니다.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=20,
    stratify=y
)
# KNeighborsClassifier(n_neighbors=7)을 사용합니다.
KN_model = KNeighborsClassifier(n_neighbors=7)
KN_model.fit(X_train, y_train)
# Scaling을 하지 않은 모델의 Test Accuracy를 계산합니다.
KN_model_acc = KN_model.score(X_test, y_test)
# StandardScaler를 Train 데이터에만 fit한 뒤 Scaling한 모델의 Test Accuracy를 계산합니다.
scaler = StandardScaler(
    copy=True,
    with_mean=True,
    with_std=True,
)
X_train_scaled = scaler.fit_transform(X_train) # 스케일 X 테이터 훈련 및 변환
X_test_scaled = scaler.transform(X_test) # 스케일 기준 테스트 데이터에 적용

scaled_model = KNeighborsClassifier(n_neighbors=7)

scaled_model.fit(X_train_scaled, y_train) #스케일된 X와 y 훈련
scaled_model_acc = scaled_model.score(X_test_scaled, y_test)

pp('scaled 전 Accuracy:',KN_model_acc)
pp('scaled 후 Accuracy:',scaled_model_acc)
# Scaling 전후 Accuracy 차이를 출력합니다.
pp('Accuracy 차이:',scaled_model_acc - KN_model_acc)
# scaler.mean과 scaler.scale 중 앞의 5개 값을 출력해 학습된 변환 기준을 확인합니다.
scaler_df = pd.DataFrame({
    'feature': X.columns,
    'mean': scaler.mean_,
    'scale': scaler.scale_
})

pp(scaler_df.round(4))
# 결과를 보고 KNN에서 Scaling이 중요한 이유를 2~3문장으로 정리합니다.
#
# 제출 결과
# Scaling 전 Accuracy
# Scaling 후 Accuracy
# Accuracy 차이
# scaler.mean, scaler.scale
# 결과 해석