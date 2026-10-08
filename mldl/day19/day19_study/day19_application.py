# day19_application.py
# 주제:온라인 쇼핑 구매 여부 예측 모델 비교
#
# [상황]
# 온라인 쇼핑몰에서 사용자의 행동 특성을 이용하여 구매 여부를 예측하려고 합니다.
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

# 1.numpy의 default_rng(42)를 이용해 800명의 가상 고객 데이터를 생성하십시오.
# 2.다음 특성을 생성하십시오.
# visits: 최근 30일 방문 횟수, 1~30 정수
# avg_view_min: 평균 상품 조회 시간, 0.5~15.0 실수
# cart_items: 장바구니 상품 수, 0~10 정수
# coupon_used: 쿠폰 사용 여부, 0 또는 1
# review_count: 작성 리뷰 수, 0~20 정수
rng = np.random.default_rng(42)
size = 800
df = pd.DataFrame({
    "visits": rng.integers(1, 31, size),
    "avg_view_min": rng.uniform(0.5, 15.0, size),
    "cart_items": rng.integers(0, 11, size),
    "coupon_used": rng.integers(0, 2, size),
    "review_count": rng.integers(0, 21, size)
})
pp(df)

# 3.다음 score를 계산하십시오.
# score = visits0.08 + avg_view_min0.25 + cart_items0.5 + coupon_used1.2 + review_count*0.05 + 정규분포 잡음
# 3. score 계산
noise = rng.normal(0, 0.5, size)
score = (
    df['visits'] * 0.08 +
    df['avg_view_min'] * 0.25 +
    df['cart_items'] * 0.5 +
    df['coupon_used'] * 1.2 +
    df['review_count'] * 0.05 +
    noise
)

# 4. score가 중앙값보다 크면 purchase=1, 아니면 0으로 만드십시오.
score_median = score.median()
purchase = np.where(score >= score_median, 1, 0)
# train_test_split으로 학습 80%, 테스트 20%를 구성하십시오.
X = df
y = purchase

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 6. Decision Tree
tree = DecisionTreeClassifier(
    max_depth=4,
    random_state=42
)

tree.fit(X_train, y_train)
tree_pred = tree.predict(X_test)


# 6. Random Forest
forest = RandomForestClassifier(
    n_estimators=150,
    random_state=42,
    n_jobs=-1
)
forest.fit(X_train, y_train)
forest_pred = forest.predict(X_test)

# 7. 두 모델의 테스트 정확도를 출력하고 어느 모델이 더 높은지 출력하십시오.
tree_acc = accuracy_score(y_test, tree_pred)
forest_acc = accuracy_score(y_test,forest_pred)
pp(tree_acc)
pp(forest_acc)
# 8랜덤포레스트의 confusion_matrix를 출력하십시오.
cm = confusion_matrix(y_test, forest_pred)
# pp(cm)

# 9 랜덤포레스트의 특성 중요도를 내림차순 DataFrame으로 출력하십시오.

importance_df = pd.DataFrame({
    'feature': df.columns,
    'importance': forest.feature_importances_,
}).sort_values(by='importance', ascending=False)
pp(importance_df)

#10.특성 중요도 상위 3개를 막대그래프로 시각화하십시오
importance_df.head(3).plot(
    x='feature',
    y='importance',
    kind='bar',
    legend=False,
)

plt.tight_layout()
plt.xticks(rotation=0)
plt.show()







