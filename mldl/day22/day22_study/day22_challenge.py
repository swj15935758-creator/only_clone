# day22_challenge.py
# 주제:채용공고 역량 패턴 군집화와 PCA 해석
#
# 상황
# IT 직무 채용공고 24개의 요구 역량 수준을 0~10 점수로 정리했습니다.
# 정답 직무 라벨 없이 채용공고의 요구 역량 패턴을 군집화하고 PCA로 시각화하려고 합니다.
#
# 데이터 생성 규칙
# numpy.random.default_rng(21)을 사용하여 아래 세 패턴의 데이터를 각각 8개씩 생성합니다.
# 단, 패턴명은 최종 DataFrame에 정답 라벨로 저장하지 않습니다.
#
# 패턴 A
# Python: 평균 8.5, 표준편차 0.7
# SQL: 평균 8.0, 표준편차 0.8
# Cloud: 평균 6.0, 표준편차 1.0
# LLM: 평균 7.5, 표준편차 0.9
# Frontend: 평균 3.0, 표준편차 1.0
#
# 패턴 B
# Python: 평균 5.5, 표준편차 0.9
# SQL: 평균 5.0, 표준편차 1.0
# Cloud: 평균 6.5, 표준편차 0.8
# LLM: 평균 4.0, 표준편차 1.0
# Frontend: 평균 8.5, 표준편차 0.7
#
# 패턴 C
# Python: 평균 7.0, 표준편차 0.8
# SQL: 평균 6.0, 표준편차 0.9
# Cloud: 평균 8.5, 표준편차 0.7
# LLM: 평균 5.5, 표준편차 0.9
# Frontend: 평균 4.5, 표준편차 1.0
#
# 모든 생성값은 clip(0, 10)으로 0~10 범위로 제한합니다.
#
# 요구사항
# 5개 특성으로 DataFrame을 생성합니다.
# 공고ID를 J001 ~ J024 형식으로 추가합니다.
# StandardScaler로 표준화합니다.
# K=3으로 KMeans를 학습하고 군집 번호를 추가합니다.
# 군집별 크기와 평균 역량 점수를 출력합니다.
# 군집 중심점을 원래 0~10 점수 단위로 복원하여 출력합니다.
# PCA(n_components=2)를 적용합니다.
# PC1과 PC2를 DataFrame에 추가합니다.
# PC1과 PC2의 설명분산비율과 누적 설명분산비율을 출력합니다.
# pca.components_를 5개 원본 역량과 연결한 DataFrame으로 출력합니다.
# 군집별 색이 구분되는 PC1-PC2 산점도를 작성합니다.
# 각 군집 평균에서 가장 높은 역량 2개를 찾아 핵심역량 문자열을 자동 생성합니다.
# 군집 번호와 자동 생성한 핵심역량을 함께 출력합니다.
# 마지막에는 새로운 채용공고 [Python=9, SQL=8, Cloud=7, LLM=9, Frontend=2]가 어느 군집에 배정되는지 예측하고 해당 군집의 핵심역량을 출력합니다.
#
# 해석 조건
# 코드 마지막 주석에 아래 내용을 각각 1~2줄로 작성합니다.
# PCA 2차원 시각화에서 군집이 겹칠 수 있는 이유
# 군집 번호를 실제 직무명으로 바로 간주하면 안 되는 이유
# day22_challenge.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from include.graph_config import set_graph
from print_util import pp


set_graph(10, 8, 13)

rng = np.random.default_rng(21)  # 과제 데이터 재현을 위한 난수 생성기
features = ["Python", "SQL", "Cloud", "LLM", "Frontend"]

pattern_a = pd.DataFrame({
    "Python": rng.normal(8.5, 0.7, 8).clip(0, 10),
    "SQL": rng.normal(8.0, 0.8, 8).clip(0, 10),
    "Cloud": rng.normal(6.0, 1.0, 8).clip(0, 10),
    "LLM": rng.normal(7.5, 0.9, 8).clip(0, 10),
    "Frontend": rng.normal(3.0, 1.0, 8).clip(0, 10)
})
pattern_b = pd.DataFrame({
    "Python": rng.normal(5.5, 0.9, 8).clip(0, 10),
    "SQL": rng.normal(5.0, 1.0, 8).clip(0, 10),
    "Cloud": rng.normal(6.5, 0.8, 8).clip(0, 10),
    "LLM": rng.normal(4.0, 1.0, 8).clip(0, 10),
    "Frontend": rng.normal(8.5, 0.7, 8).clip(0, 10)
})
pattern_c = pd.DataFrame({
    "Python": rng.normal(7.0, 0.8, 8).clip(0, 10),
    "SQL": rng.normal(6.0, 0.9, 8).clip(0, 10),
    "Cloud": rng.normal(8.5, 0.7, 8).clip(0, 10),
    "LLM": rng.normal(5.5, 0.9, 8).clip(0, 10),
    "Frontend": rng.normal(4.5, 1.0, 8).clip(0, 10)
})
df = pd.concat([pattern_a, pattern_b, pattern_c], ignore_index=True)  # 패턴명은 정답 라벨로 보존하지 않음
df[features] = df[features].round(2)
df["공고ID"] = [f"J{i:03d}" for i in range(1, len(df) + 1)]

scaler = StandardScaler()  # 5개 역량 점수의 상대적 차이를 같은 거리 기준으로 변환
X_scaled = scaler.fit_transform(df[features])

model = KMeans(
    n_clusters=3,  # 세 가지 역량 패턴을 찾기 위한 군집 수
    n_init=10,  # 초기 중심점 변화에 따른 불안정성을 낮추는 반복 학습 횟수
    random_state=42  # 동일한 결과를 재현하기 위한 난수 고정
)
df["군집"] = model.fit_predict(X_scaled)

pp("군집별 채용공고 수")
pp(df["군집"].value_counts().sort_index())

cluster_summary = df.groupby("군집")[features].mean().round(2)
pp("군집별 평균 요구 역량")
pp(cluster_summary)

centers = scaler.inverse_transform(model.cluster_centers_)  # 표준화 공간의 중심을 0~10 원래 점수로 복원
center_df = pd.DataFrame(centers, columns=features).round(2)
center_df.index.name = "군집"
pp("원래 점수 단위 군집 중심")
pp(center_df)

pca = PCA(
    n_components=2,  # 5개 역량 특성을 2개의 주성분으로 축소해 시각화
    svd_solver="auto"
)
X_pca = pca.fit_transform(X_scaled)
df["PC1"] = X_pca[:, 0]
df["PC2"] = X_pca[:, 1]

ratio = pd.Series(pca.explained_variance_ratio_, index=["PC1", "PC2"]).round(4)
pp("PCA 설명분산비율")
pp(ratio)
pp("PC1+PC2 누적 설명분산비율:", round(float(ratio.sum()), 4))

component_df = pd.DataFrame(
    pca.components_,  # 각 주성분이 원본 5개 역량을 얼마나 가중해 구성되는지 표현
    index=["PC1", "PC2"],
    columns=features
).round(4)
pp("PCA 주성분 구성 가중치")
pp(component_df)

for cluster_id in sorted(df["군집"].unique()):
    part = df[df["군집"] == cluster_id]
    plt.scatter(
        part["PC1"],
        part["PC2"],
        label=f"Cluster {cluster_id}",
        alpha=0.75,
        s=60
    )
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("채용공고 요구 역량 군집 - PCA 시각화")
plt.legend()
plt.grid(alpha=0.25)
plt.tight_layout()
plt.show()

cluster_keywords = {}
for cluster_id, row in cluster_summary.iterrows():
    top2 = row.sort_values(ascending=False).head(2).index.tolist()  # 군집 평균이 가장 높은 역량 2개 추출
    cluster_keywords[cluster_id] = " + ".join(top2)

keyword_df = pd.DataFrame({
    "군집": list(cluster_keywords.keys()),
    "핵심역량": list(cluster_keywords.values())
}).sort_values("군집")
pp("군집별 자동 생성 핵심역량")
pp(keyword_df)

new_job = pd.DataFrame([{
    "Python": 9,
    "SQL": 8,
    "Cloud": 7,
    "LLM": 9,
    "Frontend": 2
}])
new_scaled = scaler.transform(new_job)  # 기존 데이터의 표준화 기준을 신규 공고에도 동일하게 적용
new_cluster = int(model.predict(new_scaled)[0])  # 학습된 군집 중심점 기준으로 신규 공고 배정
pp("신규 채용공고 배정 군집:", new_cluster)
pp("신규 채용공고 군집 핵심역량:", cluster_keywords[new_cluster])

# PCA 2차원 표현은 5차원 원본 정보의 일부를 버리므로 원래 공간에서 분리된 군집이 겹쳐 보일 수 있습니다.
# 군집 번호는 알고리즘이 임의로 부여한 식별값이므로 평균 특성을 해석한 뒤 실제 직무 의미를 별도로 붙여야 합니다.


