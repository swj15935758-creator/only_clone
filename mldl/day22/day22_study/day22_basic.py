# day22_basic.py
# 주제:학습공간 이용 패턴 군집화
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from print_util import pp

# 상황
# 대학 내 학습공간 이용 기록을 바탕으로 이용 패턴이 유사한 그룹을 찾으려고 합니다.
# 정답 라벨은 없으며 다음 3개 특성을 사용합니다.

# 데이터
# 주간도서관방문: [6, 7, 5, 1, 2, 1, 4, 5, 4, 2, 3, 2]
# 일평균열람시간: [220, 245, 210, 45, 60, 50, 150, 170, 140, 80, 95, 75]
# 온라인강의시간: [3, 2, 4, 10, 9, 11, 6, 5, 7, 8, 7, 9]

# 요구사항
# pandas DataFrame을 생성합니다.
df = pd.DataFrame({
    '주간도서관방문': [6, 7, 5, 1, 2, 1, 4, 5, 4, 2, 3, 2],
    '일평균열람시간': [220, 245, 210, 45, 60, 50, 150, 170, 140, 80, 95, 75],
    '온라인강의시간': [3, 2, 4, 10, 9, 11, 6, 5, 7, 8, 7, 9]
})
# StandardScaler를 사용해 3개 특성을 표준화합니다.
scaler = StandardScaler(
    copy=True, # 원본배열 보존하고 변환 결과를 새로 생성 > 복사해서 작업
    with_mean=True, # 각 특성의 평균을 0 에 가깝게 이동
    with_std=True, # 각 특성의 값을 표준편차로 나눠서 스케일 조정
)
X_scaled = scaler.fit_transform(df) # 값 스케일링
# KMeans(n_clusters=3, random_state=42, n_init=10)로 군집화합니다.
library_model = KMeans(
    n_clusters=3,
    n_init=10,
    random_state=42
)
# 각 행에 군집 컬럼을 추가합니다.
clusters = library_model.fit_predict(X_scaled) # 군집 이후 값 저장 시리즈로
df['군집'] = clusters
# pp(df)
# 군집별 데이터 수를 출력합니다.
pp(df['군집'].value_counts().sort_index())
# 군집별 3개 특성의 평균을 출력합니다.
cluster_mean = df.groupby('군집').mean()
pp(cluster_mean)
# 군집 중심점을 원래 단위로 복원하여 DataFrame으로 출력합니다.
centers = scaler.inverse_transform(library_model.cluster_centers_)
centers_df = pd.DataFrame(
    centers,
    columns=['주간도서관방문', '일평균열람시간', '온라인강의시간']
)
pp(centers_df)
