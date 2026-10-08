# day19_basic.py
# 주제:제조 공정 품질 판정용 의사결정트리
#
# [상황]
# 한 제조 공정에서 온도, 압력, 생산 속도, 원료 수분율을 이용해 제품의 품질 합격 여부를 예측하려고 합니다.
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

# 1.numpy의 default_rng(42)를 이용해 300개의 데이터를 생성하십시오.
# 2.다음 범위로 특성을 생성하십시오.
#     temperature: 60~100 사이 실수
#     pressure: 80~140 사이 실수
#     speed: 20~80 사이 실수
#     moisture: 2~12 사이 실수

rng = np.random.default_rng(42)
size = 300
df = pd.DataFrame({
    "temperature": rng.uniform(60, 100, size),
    "pressure": rng.uniform(80, 140, size),
    "speed": rng.uniform(20, 80, size),
    "moisture": rng.uniform(2, 12, size)
})


# 3. 합격 여부 quality를 다음 규칙으로 만드십시오.
#     temperature가 70 이상 90 이하
#     pressure가 95 이상 125 이하
#     moisture가 9 미만
# 위 세 조건을 모두 만족하면 1, 아니면 0으로 지정하십시오

def quality(X):
    y = []
    for index, row in X.iterrows():
        if ((row['temperature'] >= 70) and (row['temperature'] <= 90) &
                (row['pressure'] >= 95) and (row['pressure'] <= 125) &
                (row['moisture'] < 9)):
            is_quality = 1
            y.append(is_quality)
        else:
            is_quality = 0
            y.append(is_quality)
    return y

# def quality(X):
#     y = np.where(
#         (X['temperature'] >= 70) &
#         (X['temperature'] <= 90) &
#         (X['pressure'] >= 95) &
#         (X['pressure'] <= 125) &
#         (X['moisture'] < 9),
#         1,
#         0
#     )
#     return y

# 4. 데이터를 DataFrame으로 구성하십시오.
# 5. X와 y를 분리하십시오.
X = df[['temperature', 'pressure','speed', 'moisture']]
y = quality(X)
# pp(y)

# 6. train_test_split을 사용해 학습 75%, 테스트 25%로 분리하십시오.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
#   stratify=y
    test_size=0.25,
#   random_state=42
    random_state=42,
    stratify=y
)

# 7. DecisionTreeClassifier(max_depth=3, random_state=42)를 학습하십시오
tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)
tree_train_pred = tree.predict(X_train)
tree_test_pred = tree.predict(X_test)

# 8. 학습 정확도와 테스트 정확도를 각각 출력하십시오.
pp(accuracy_score(y_train, tree_train_pred))
pp(accuracy_score(y_test, tree_test_pred))

# 9. featureimportances를 이용해 특성 중요도를 내림차순으로 출력하십시오.
importance_df = pd.DataFrame({
    'feature': X.columns,
    'importance': tree.feature_importances_,
}).sort_values(by='importance', ascending=False)

pp(importance_df)

# 10. 가장 중요한 특성 1개의 이름을 출력하십시오
best_index = importance_df['importance'].idxmax()
best_feature = importance_df.loc[best_index, 'feature']
pp(best_feature)