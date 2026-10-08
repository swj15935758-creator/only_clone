# day18_application.py
# 주제:AI휴먼 day18 Application 과제
# 주제: 와인 품종 KNN 분류

import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from python.print_util import pp
from sklearn.datasets import load_wine

# 목표
# Wine 데이터를 사용하여 KNN의 K값에 따라 분류 정확도가 어떻게 달라지는지 비교합니다.
# https://scikit-learn.org/stable/datasets/toy_dataset.html
#
# 요구사항
#
# load_wine(as_frame=True)로 데이터를 불러옵니다.
df_wine = load_wine(as_frame=True)

# 다음 5개 특성만 사용합니다.
X = df_wine.data[['alcohol','malic_acid','total_phenols','color_intensity','hue']] # X 데이터프레임
y = df_wine.target # y 타겟

# alcohol
# malic_acid
# total_phenols
# color_intensity
# hue
# 정답은 target을 사용합니다.

X_train,X_test,y_train,y_test = train_test_split(
    X,
    y,
# 학습 데이터 75%, 테스트 데이터 25%로 분리합니다.
    test_size=0.25,
# random_state=42, stratify=y를 적용합니다.
    random_state=42,
    stratify=y
)

k_accuracy_list = []
K_list = [1,3,5,7,9,11]

# K값을 [1, 3, 5, 7, 9, 11]로 변경하면서 각각의 정확도를 계산합니다.
for K in K_list:
    knn = KNeighborsClassifier(
        n_neighbors=K,  # 참고할 가장 가까운 이웃의 (K)수
    )
    knn.fit(X_train,y_train)
    knn_pred = knn.predict(X_test)
    k_accuracy = accuracy_score(y_test,knn_pred)
    k_accuracy_list.append(k_accuracy)

# 결과를 K, 정확도 컬럼을 가진 DataFrame으로 정리합니다.
result = pd.DataFrame({
    'K':K_list,
    '정확도':k_accuracy_list
})

pp(result)

# 가장 높은 정확도를 가진 K값과 정확도를 출력합니다.
best_knn_index = k_accuracy_list.index(max(k_accuracy_list))
best_K = K_list[best_knn_index]
best_accuracy = k_accuracy_list[best_knn_index]

pp('가장 좋은 K:',best_K)
pp('가장 높은 정확도:',best_accuracy)


# 가장 좋은 K값으로 모델을 다시 학습합니다.
best_knn = KNeighborsClassifier(
    n_neighbors=best_K,  # 참고할 가장 가까운 이웃의 (K)수
    weights='uniform',  # 각이웃의 가중치 동일하게 적용
    metric='minkowski',  # 거리 계산 알고리즘
    p=2  # Euclidean Distance : 두점 사이의 거리 (직선거리)
)

best_knn.fit(X_train,y_train)

# 가장 좋은 K값 모델의 전체 테스트 데이터 예측
best_knn_pred = best_knn.predict(X_test)

# 가장 좋은 K값 모델의 정확도
best_k_accuracy = accuracy_score(y_test,best_knn_pred)
pp('최종 모델 정확도:',best_k_accuracy)

# 가장 좋은 K값으로 모델을 다시 학습한 뒤 테스트 데이터 앞 10건의 실제값과 예측값을 비교합니다.
best_knn_pred_10 = best_knn.predict(X_test.head(10))

comparison = pd.DataFrame({
    '실제값': y_test.head(10).to_numpy(),
    '예측값': best_knn_pred_10
})

pp(comparison)

# 컬럼명
#
# alcohol        알코올 함량
# malic_acid        말산
# total_phenols    총 페놀
# color_intensity    색상 강도
# hue        색조
# target        와인 품종