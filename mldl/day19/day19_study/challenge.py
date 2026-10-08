# challenge.py
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

set_graph(10,8,13)

# 42를 시드로 하는 랜덤 제네레이터
rng = np.random.default_rng(42)

size = 1200

df = pd.DataFrame({
    'overtime' : rng.integers(0,2,size),
    'satisfaction' : rng.uniform(1,10,size),
    'monthly_income' : rng.uniform(250,900,size),
    'years_company' : rng.integers(0,21,size),
    'projects' : rng.integers(1,9,size),
    'commute_min' : rng.uniform(10,120,size),
})
pp(df.head(10))

# 이직 위험과 관련된 가상 규칙에 잡음을 추가해 현실적인 분류 경계를 구성
risk = (
    df['overtime'] * 1.8
    - df['satisfaction'] * 0.35
    - df['monthly_income'] * 0.004
    - df['years_company'] * 0.08
    + df['projects'] * 0.18
    + df['commute_min'] * 0.015
    + rng.normal(0,0.9,size) # 잡음 : 방해해주는 데이터
)
pp(risk)

# 임계값
threshold = np.quantile(risk, 0.65)
pp(threshold)

# 조건이 True면1 , 조건이 False 면 0
df['attrition'] = (risk > threshold).astype(int)
pp(df['attrition'])
X = df.drop(columns = 'attrition')
y = df['attrition']
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size = 0.25,
    random_state = 42,
    stratify = y,
)


# model
# 3개의 모델을 딕셔너리로 만든것 하니씩 꺼내서 for문으로 한번에 처리 하도록 만들기 위해 함수로도 변형가능
models = {
     'Deep Tree' : DecisionTreeClassifier(random_state=42),
    'Controlled Tree' : DecisionTreeClassifier(
        max_depth = 5,
        min_samples_leaf = 2,
        random_state=42),
    'Random Forest' : RandomForestClassifier(
        n_estimators = 300,
        max_depth = 8,
        min_samples_leaf = 3,
        random_state=42,
        n_jobs=-1
    )
}

rows =[] # 결과 저장 리스트
for name, model in models.items():
    model.fit(X_train, y_train)
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    rows.append({
        'model' : name,
        'train_acc' : train_acc,
        'test_acc' : test_acc,
        'gap' : train_acc - test_acc,
    })

# 결과 데이터 프레임
result_df = (
    pd.DataFrame(rows)
    .sort_values(by = 'test_acc', ascending = False)
    .reset_index(drop = True)
)

pp(result_df.round(4))


# 학습/테스트 정확도 차이가 큰 모델
largest_gap_model = result_df.loc[result_df['gap'].idxmax(),'model']
pp(largest_gap_model) # Deep Tree

# 테스트 정확도가 가장 높은 모델
best_test_model = result_df.loc[result_df['test_acc'].idxmax(),'model']
pp(best_test_model)  # Random Forest

forest = models['Random Forest'] # 랜덤 포레스트

# 패쳐 중요도 데이터 프래임
importance_df = pd.DataFrame({
    'feature' : X.columns,
    'importance' : forest.feature_importances_
}).sort_values(by = 'importance', ascending = False).reset_index(drop = True)

# 특성 중요도
pp(importance_df.round(4))

# 특성 중요도 상위 3개
pp(importance_df.head(3).round(4))

top3 = importance_df.head(3).sort_values(by = 'importance', ascending = False)

# plt.barh(top3['feature'], top3['importance'])
# plt.xlabel("Feature Importance")
# plt.ylabel("Feature")
# plt.title('직원 이직 예측 - 중요 특성 상위 3개')
# plt.tight_layout
# plt.show()

new_employee = pd.DataFrame([{
    'overtime': 1,
    'satisfaction': 4.0,
    'monthly_income': 420,
    'years_company': 2,
    'projects': 6,
    'commute_min': 80
}])

pred = forest.predict(new_employee)[0] # 예측클래스
prob = forest.predict_proba(new_employee)[0] # 예측클래스 확률

# 이직 클래스(1)의 위치
class_index = list(forest.classes_).index(1)

attrition_prob = prob[class_index]

pp('[신규 직원 예측]')
pp(new_employee)

pp(f'예측 이직 여부: {pred}')
pp(f'이직 확률: {attrition_prob:.4f}')

# 단일 깊은 트리는 특정 학습 샘플과 잡음에 민감하지만
# 랜덤 포레스트는 서로 다른 여러 트리의 예측을 결합해 변동성을 줄일 수 있음

# feature_importances_는 모델 분기에 대한 상대적 기여도이므로
# 해당 특성이 실제 결과를 직접 유발한다는 인과관계를 의미하지 않는다












