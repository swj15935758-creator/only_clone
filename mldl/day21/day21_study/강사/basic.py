# day21_basic.py

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from print_util import pp



# 가상 센서 데이터 생성
X_array, y = make_classification(
    n_samples=600,       # 전체 설비 측정 건수
    n_features=5,        # 센서 특성 개수
    n_informative=4,     # 분류에 실제 정보를 주는 특성 수
    n_redundant=0,       # 다른 특성의 조합으로 만들어지는 중복 특성 수
    class_sep=1.2,       # 두 클래스 사이의 분리 정도
    random_state=20
)
X = pd.DataFrame(X_array, columns=["진동", "온도", "압력", "전류", "소음"])
pp(X.shape)
X["진동"] *= 1000      # 큰 단위의 센서를 가정해 스케일 차이를 만듦
X["소음"] *= 0.01      # 매우 작은 단위의 센서를 가정
pp("특성별 표준편차")
pp(X.std().round(3))

# train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=20,
    stratify=y,
)

# Scaling 적용하지 않은 KNN
raw_model = KNeighborsClassifier(n_neighbors=7)
raw_model.fit(X_train, y_train)
raw_pred = raw_model.predict(X_test)
raw_accuracy = accuracy_score(y_test, raw_pred)

# Train 데이터에서만 Scaling 기준 학습
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
scaled_model = KNeighborsClassifier(n_neighbors=7)
scaled_model.fit(X_train_scaled, y_train)
scaled_pred = scaled_model.predict(X_test_scaled)
scaled_accuracy = accuracy_score(y_test, scaled_pred)

# 결과 확인
pp('Scaling 전 Accuracy: ',round(raw_accuracy,4))
pp('Scaling 후 Accuracy: ',round(scaled_accuracy,4))
pp('Accuracy 차이: ',round(scaled_accuracy-raw_accuracy,4))
pp('scaler.mean_:',pd.Series(scaler.mean_,index=X.columns).round(4))
pp('scaler.scale_:',pd.Series(scaler.scale_,index=X.columns).round(4))

# 해석
pp('[해석]')
pp('KNN은 특성 간 거리를 사용하므로 값의 범위가 큰 센서가 거리 계산을 지배할 수 있습니다.')
pp('StandardScaler를 적용하면 각 특성이 비슷한 스케일에서 거리 계산에 참여하여 더 공정한 비교가 가능합니다.')




























