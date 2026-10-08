# day22_application.py
# 주제:설비 운전 패턴 분석과 적절한 군집 수 검토
#
# 상황
# 생산 설비 18대의 운전 데이터를 기반으로 비슷한 운전 패턴을 가진 설비 그룹을 찾으려고 합니다.
#
# 데이터
# 전력사용량: [82, 88, 79, 85, 91, 86, 42, 38, 45, 41, 39, 44, 65, 69, 63, 71, 67, 66]
# 평균온도: [74, 77, 72, 75, 79, 76, 48, 45, 51, 47, 46, 50, 61, 64, 59, 66, 63, 62]
# 진동수준: [6.8, 7.2, 6.5, 7.0, 7.6, 7.1, 2.1, 1.8, 2.4, 2.0, 1.9, 2.3, 4.2, 4.6, 4.0, 4.9, 4.5, 4.3]
# 일가동시간: [20, 21, 19, 22, 21, 20, 8, 7, 9, 8, 7, 9, 14, 15, 13, 16, 15, 14]
#
# 요구사항
# DataFrame을 생성하고 4개 특성을 StandardScaler로 표준화합니다.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from print_util import pp
from include.graph_config import set_graph

set_graph(10, 8, 13)


df = pd.DataFrame({
    '전력사용량': [82, 88, 79, 85, 91, 86, 42, 38, 45, 41, 39, 44, 65, 69, 63, 71, 67, 66],
    '평균온도': [74, 77, 72, 75, 79, 76, 48, 45, 51, 47, 46, 50, 61, 64, 59, 66, 63, 62],
    '진동수준': [6.8, 7.2, 6.5, 7.0, 7.6, 7.1, 2.1, 1.8, 2.4, 2.0, 1.9, 2.3, 4.2, 4.6, 4.0, 4.9, 4.5, 4.3],
    '일가동시간': [20, 21, 19, 22, 21, 20, 8, 7, 9, 8, 7, 9, 14, 15, 13, 16, 15, 14]
})

features = ['전력사용량', '평균온도', '진동수준', '일가동시간']

scaler = StandardScaler(
    copy=True,       # 원본 데이터를 보존하고 변환 결과를 새로 생성
    with_mean=True,  # 각 특성의 평균을 0에 가깝게 이동
    with_std=True,   # 각 특성을 표준편차 기준으로 스케일 조정
)

X_scaled = scaler.fit_transform(df[features])

pp('원본 데이터')
pp(df)

pp('표준화 후 shape')
pp(X_scaled.shape)


# K를 2~5까지 변경하면서 KMeans를 학습합니다.
K_list = list(range(2, 6))

drive_values = [
    KMeans(
        n_clusters=k,
        n_init=10,
        random_state=42
    ).fit(X_scaled)
    for k in K_list
]


# 각 K에 대해 Inertia와 Silhouette Score를 계산해 DataFrame으로 출력합니다.
silhouette_values = []

for model in drive_values:
    score = silhouette_score(
        X_scaled,
        model.labels_
    )
    silhouette_values.append(score)


inertia_values = []

for model in drive_values:
    inertia_values.append(model.inertia_)


# DataFrame 생성
result_df = pd.DataFrame({
    'K': K_list,
    'Inertia': inertia_values,
    'Silhouette Score': silhouette_values
})

pp('K별 평가 결과')
pp(result_df.round(3))


# K가 하나 증가할 때 Inertia 감소량
decrease_values = -np.diff(inertia_values)

pp('인접 K로 갈 때 Inertia 감소량')
pp(np.round(decrease_values, 3))


# Silhouette Score가 가장 높은 K를 자동으로 선택합니다.
best_index = result_df['Silhouette Score'].idxmax()

best_K = result_df.loc[
    best_index,
    'K'
]

pp('Silhouette Score가 가장 높은 K')
pp(best_K)


# 선택된 K로 최종 KMeans 모델을 다시 학습합니다.
final_model = KMeans(
    n_clusters=best_K,
    n_init=10,
    random_state=42
)

final_labels = final_model.fit_predict(X_scaled)


# 각 설비의 군집 번호를 DataFrame에 추가합니다.
df['군집'] = final_labels

pp('설비별 군집 번호')
pp(df)


# 군집별 데이터 수와 평균 특성을 출력합니다.
cluster_size = df['군집'].value_counts().sort_index()

pp('군집별 설비 수')
pp(cluster_size)


cluster_mean = df.groupby('군집')[features].mean().round(2)

pp('군집별 평균 특성')
pp(cluster_mean)


# K별 Inertia 그래프
plt.figure(figsize=(7, 4))

plt.plot(
    K_list,
    inertia_values,
    marker='o'
)

plt.xlabel('군집 수 K')
plt.ylabel('Inertia')
plt.title('K별 Inertia')
plt.xticks(K_list)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# K별 Silhouette Score 그래프
plt.figure(figsize=(7, 4))

plt.plot(
    K_list,
    silhouette_values,
    marker='o'
)

plt.xlabel('군집 수 K')
plt.ylabel('Silhouette Score')
plt.title('K별 Silhouette Score')
plt.xticks(K_list)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# Silhouette Score는 군집의 응집도와 분리도를 평가하지만 실제 설비 운영 목적까지 반영하지는 않습니다.
# 따라서 Inertia 변화, 군집별 특성, 업무상 해석 가능성도 함께 고려하여 K를 결정해야 합니다.