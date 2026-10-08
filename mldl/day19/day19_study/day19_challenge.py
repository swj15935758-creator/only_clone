# day19_challenge.py
# 주제:직원 이직 위험 예측과 중요 특성 해석
#
# [상황]
# 기업의 인사 데이터를 이용해 직원의 이직 위험을 예측하고, 어떤 특성이 예측에 크게 기여하는지 분석하려고 합니다.
#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from include.graph_config import set_graph
from print_util import pp

# 1. numpy의 default_rng(42)를 이용해 1,200명의 가상 직원 데이터를 생성하십시오.
# 2. 다음 특성을 생성하십시오.
# overtime: 야근 여부, 0 또는 1
# satisfaction: 업무 만족도, 1~10 실수
# monthly_income: 월 급여, 250~900 사이 실수
# years_company: 근속연수, 0~20 정수
# projects: 담당 프로젝트 수, 1~8 정수
# commute_min: 출퇴근 시간, 10~120 실수

size = 1200
rng = np.random.default_rng(42)
df = pd.DataFrame({
    "overtime": rng.integers(0, 2, size),
    "satisfaction": rng.uniform(1, 10, size),
    "monthly_income": rng.uniform(250, 900, size),
    "years_company": rng.integers(0, 21, size),
    "projects": rng.integers(1, 9, size),
    "commute_min": rng.uniform(10, 120, size)
})
# 3. 이직 위험 점수를 다음과 같이 구성하십시오.
# risk = overtime1.8 - satisfaction0.35 - monthly_income0.004 - years_company0.08 + projects0.18 + commute_min0.015 + 정규분포 잡음
noise = rng.normal(0, 0.5, size)
risk = (
        df['overtime']*1.8 -
        df['satisfaction']*0.35 -
        df['monthly_income']*0.004 -
        df['years_company']*0.08 +
        df['projects']*0.18 +
        df['commute_min']*0.015 +
        noise
        )
# 4. risk가 전체 값의 65% 분위수보다 크면 attrition=1, 아니면 0으로 만드십시오
risk_over = risk.quantile(0.65)
attrition = np.where(risk > risk_over ,1,0)
# 5. train_test_split을 사용해 학습 75%, 테스트 25%로 분리하십시오.
df_columns = df.columns.to_list()
# y값  타겟 만들기
y_n = np.where(risk > risk_over,1,0) # n 배열
y=pd.Series(y_n) # 시리즈
# X데이터 프레임
X= df[df_columns]
# train_test_split을 사용해 학습 75%, 테스트 25%로 분리하십시오.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)
# 6.다음 세 모델을 각각 학습하십시오.
tree = DecisionTreeClassifier(random_state=42)
tree.fit(X_train, y_train) # 학습
tree58 = DecisionTreeClassifier(max_depth=5, min_samples_leaf=8, random_state=42)
tree58.fit(X_train, y_train) # 학습
forest = RandomForestClassifier(n_estimators=300, max_depth=8, min_samples_leaf=3, random_state=42, n_jobs=-1)
forest.fit(X_train, y_train) # 학습
#7. 세 모델의 학습 정확도와 테스트 정확도를 표 형태 DataFrame으로 비교하십시오.
# 훈련 정확도
tree_acc = accuracy_score(y_train,tree.predict(X_train))
tree58_acc = accuracy_score(y_train,tree58.predict(X_train))
forest_acc = accuracy_score(y_train,forest.predict(X_train))
#테스트 정확도
tree_acc_t = accuracy_score(y_test,tree.predict(X_test))
tree58_acc_t = accuracy_score(y_test,tree58.predict(X_test))
forest_acc_t = accuracy_score(y_test,forest.predict(X_test))

comparison_df = pd.DataFrame({
    '모델' : ['tree','tree58','forest'],
    '정확도':[tree_acc,tree58_acc,forest_acc],
    '테스트정확도':[tree_acc_t,tree58_acc_t,forest_acc_t],
})
# pp(comparison_df)
# 학습 정확도와 테스트 정확도의 차이(train_acc - test_acc)를 gap 컬럼으로 추가하십시오.
comparison_df['gap'] = comparison_df['정확도'] - comparison_df['테스트정확도']
# pp(comparison_df)
# 9.가장 gap이 큰 모델과 테스트 정확도가 가장 높은 모델을 각각 출력하십시오.
best_gap_index = comparison_df['gap'].idxmax()
best_acc_index = comparison_df['테스트정확도'].idxmax()
pp(best_gap_index,best_acc_index)
pp(comparison_df['gap'][best_acc_index],comparison_df['테스트정확도'][best_acc_index])

# 10.랜덤포레스트의 featureimportances를 내림차순으로 정리하십시오
importance_df = pd.DataFrame({
    'feature': df.columns,
    'importance': forest.feature_importances_,
}).sort_values(by='importance', ascending=False)
pp(importance_df)
# 11. 중요도 상위 3개 특성을 출력하고 막대그래프로 시각화하십시오
# importance_df.head(3).plot(
#     x='feature',
#     y='importance',
#     kind='bar',
#     legend=False,
# )
# plt.xticks(rotation=0)
# plt.show()

# 12.다음 신규 직원의 이직 여부와 이직 확률을 랜덤포레스트로 예측하십시오.
new_X =pd.DataFrame({
    'overtime':[1],
    'satisfaction':[4.0],
    'monthly_income':[420],
    'years_company':[2],
    'projects':[6],
    'commute_min':[80],
})
new_y = forest.predict(new_X)
pp(new_y)

# 단일 깊은 트리는 하나의 학습 데이터에 맞춰 학습하기 때문에 과적합되기 쉽다.
# 랜덤포레스트는 여러 개의 트리를 서로 다른 데이터와 특성을 이용해 학습하고,
# 여러 트리의 예측 결과를 종합하기 때문에 단일 트리보다 안정적인 예측을 할 수 있다.

# feature_importances_는 모델이 예측할 때 각 특성을 얼마나 중요하게 사용했는지를 나타낸다.
# 특성의 중요도가 높다고 해서 그 특성이 결과의 직접적인 원인이라는 뜻은 아니다.
# 따라서 feature_importances_는 예측에 대한 중요도로 해석해야 하며 인과관계로 해석하면 안 된다.








