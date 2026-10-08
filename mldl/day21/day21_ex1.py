# day21_ex1.py
# 주제: 스케일링, 교차검증, Popline, 과적합, 하이퍼파라미터 튜닝
# 1. 전체 흐름
'''
1) 데이터 준비
2) 학습/테스트
3) 스케일링(Scaling)
4) 모델 학습
5) 교차검증(Cross Validation)
6) Pipeline 구성
7) 과적합(Overfitting) 확인
8) 하이퍼파라미터(Hyper Parameter) 조정
9) GridSearchCV 로 최적 하이퍼파라미너 조합 / 몯[ㄹ 팀섹
'''

# 2. 스케일링
'''
- 스케일링은 서로 다른 범위를 가진 특성의 값 범위를 비슷한 수준으로 맞추는 전처리 과정
- 예) 키: 150~190, 연봉:30,000,000 ~ 100,000,000
        - 연봉값이 수치적으로 매우 크기 때문에 거리 기반 알고리즘에서는 연봉의 영향력이
            지나치게 커질수 있음
        - 스케일링 중요한 알고리즘
            : KNN, K-means, SVM, Logistic Regression, Neural Network, PCA
        - 영향이 상대적으로 적은 알고리즘
            : Decision Tree, Random Forest, Gradient Boosting 계열
'''
# 3.  StarndardScaler
'''
- StandardScaler 는 데이터 평균0, 표쥰편차 1인 형태로 변환
- 공식 : z= ( x - 평균) / 표준편차
- 예 편균이 70, 표준편차 10, 원래점수는 80
        - z= (80 - 70) / 10 = 1 (즉, 평균보다 표준편차 1만큼 높은 값을 의미)
- 주요 메소드
    - fit(X) : X 데이터에서 평균과 표준편차를 계산 ( train 데이터셋에만 해야함!!!)
    - transform(X) : fit(X) 에서 계산한 평균과 표준편차를 이용해 데이터를 변환
    - fit_transform(X) : fit(X) 수행 후 transform(X) 수행
    - inverse_transform(X) : 스케일링된 데이터를 원래 값으로 복원
'''
# 4. fit과 transform을 구분해야 하는 이유
'''
- 학습 데이터에서는 fit_transform을 사용하고 테스트 데이터 에는 transform()만 사용해야함
- 테스트 데이터에서도 평균과 표준편차를 다시 계산하면 테스트 데이터의 정보를 모델 평가에 사용하므로
    과적함 문제 발생
'''
# 5. 데이터 누수(Data Leakage)
'''
- 모델 데이터 학습 과정에서 원래 알 수 없어야 하는 테스트 데이터 정보가 학습 과정에 들어가는 문제
- 전체 데이터에 먼져 StandardScaler를 적용한 후 train/test 분라히면
    테스트 데이터 평균과 표준편차 정보가 학습 데이터에 반영 될 수 있음 > 과적합 문제 발생 가능
'''
# 6. 교차검중 (Cross Vaildation)
'''
- 데이터를 여러 부분으로 나누고 학습용과 검증용 역할을 번갈아 수행하면서 모델 여러번 평가하는 방법
    동일 데이터 > 여러번 분리> 여러번평가
- 목적 : 한번의 train/test 분리 결과에 의존하지 않도록 해서
    모델의 일반화 성능을 더 안정적으로 평가하기 위해 사용함
'''
# K-Fold CV
'''
- K-Fold는 데이터를 K 개로 나눈후 각 Fold를 한번씩 검증 데이터로 사용
- 예) 5개의 폴드 > 1개 검증, 나머지는 학습 ... 번갈아서
- 총 5 개의 평가 점수가 생성되고 일반적으로 최종 성능 지표로 사용
'''
# 8. cross_vak_score()
'''
- 교차검증을 간단히 수행하는 함수
- 주요 파라미터
    estimator: 평가할 머신러닝 모델, X: 입력데이터, y:정답데이터, cv:교차검증 회수
    scoring: 평가기준
        분류 : (accuracy, precision, recall, fi, roc_auc))
        회귀 : r2, neg_mean_absolute_error, neg_mean_squared_error
'''
# 9. StratifiedKFold
'''
- 분류 문제에서 각 Fold가 원래 데이터의 클래스 비율을 최대한 유지하도록 나누는 방식
- 예를 들어 전체 데이터가 정상 80%, 불량 20% 라면 각 Fold도 가능하면 
    정상 80%, 불량 20% 비율을 유지하도록 나눔
- 클래스 비율이 불균형한 데이터에서 일반 K-Fold를 사용하면 특정 Fold에
    특정 클래스가 너무 많거나 너무 적어지는 문제가 발생
- 주요 파라미터
    n_splits:Fold 개수, shuffle: 데이터를 섞을지 여부, random_state: 재현성 확보를 위한 난수 시드값
'''
# 10. Pipline
'''
- 여러 전처리 단계와 머신러닝 모델을 하나의 작업 흐름으로 연결하는 기능
- 파이프라인을 사용하는 이유
    1) 코드가 간결해 짐
    2) 전처리와 모델을 하나의 객체처럼 묶어서 사용할 수 있음
    3) 교차검증 과정에서 데이터 누수를 방지 할 수 있음
    4) GridSearchCV와 결합하기 쉬움
    5) 실무 배포 시 동일한 전처리 과정을 보장하기 쉬움
- make_pipline(): 각 단계에서 이름을 자동으로 생성하면서 파이프라인을 생성
- Pipline(): 각 단계의 이름을 지정하면서 파이프라인을 생성
'''
# 11. 일반화 (Generalization)
'''
- 학습에 사용되지 않은 새로운 데이터에서도 좋은 성능을 유지하는 능력 => 머신러닝의 궁국의 목표!!!
- 머신러닝의 궁국의 목표는 학습 데이터의 점수를 높이는 것이 아니라 일반화 성능을 높이는 것
'''
# 12. Nias와 Variance
'''
- Bias(편향) : 모델이 지나치게 단순해서 발생하는 오차, Bias 높음 => 과소적합
- Variance(분산) : 학습 데이터 변화에 모델이 지나치게 민감한 정도, Variance 높음 => 과적합
'''
# 13. 하이퍼파라미터( Hyper Parameter)
'''
- 모델이 학습하기 전에 사람이 설정해야 하는 값, 즉 모델의 설정 입력값
- LogisticRegression : C, max_iter, solver
- DecisionTreeClassifier : max_depth, min_samples_split, min_samples_leaf...
- KNeighborsClassifier : n_neighbors, weights ...
'''
# 14. 파라미터(Parameter)
'''
- 모델이 학습 과정에서 자동으로 학습하는 값
- LinearRegression : coef_, intercept_ ...
- DecisionTreeClassifier : tree_, feature_importances_ ...
- RandomForestClassifier : estimators_, feature_importances_ ...
'''
# 15. 튜닝 (Tunning)
'''
- 하이퍼 파라미터의 값을 변경하면서 가장 좋은 성능을 내는 조합을 찾는 과정
- 모든 하이퍼파라미터의 값의 범위를 다 사용하지 말고 적절한 범위를 사용해서 조합을 찾는게 중요
'''
# 16. GridSearchCV
'''
- GridSearch + Cross Validation
- GridSearch : 하이퍼파라미터들의 조합 생성해서 결합
- Cross Validation : 교차검증
'''
# 17. Pipeline의 하이퍼 파라미터 이름
'''
- '단계이름__파라미터이름' 형식으로 사용
- 일반적으로 딕셔너리를 생성해서 키를 '단계이름__파라미터이름' 으로
    값을 하이퍼파라미터의 개별값들의 리스트로 지정    
'''
# 18. GridSearchCV 주요속성
'''
- best_params_ : 가장 좋은 하이퍼파라미터 조합
- best_score_ : 가장 좋은 교차검증 평균 점수
- best_estimator_ : 가장 좋은 하이퍼파라미터가 적용된 최종 모델
- cv_results_ : 모든 조합의 평가 결과
'''
# 19. GridSearchCV의 주요 파라미터
'''
- estimator : 튜닝할 모델 또는 Pipeline
- Param_grid : 탐색할 하이퍼파라미터 후보
- cv : 교차검증 회수 = 폴드 수
- scoring : 평가기준, 여러개면 리스트
- n_jobs : 병렬 처리에 사용할 CPU 코어 수
- verbose : 진행 상황 출력 수준
'''
# 20. Regularization (정규화)
'''
- 모델이 지나치게 복잡해 지는 것을 방지하기 위해 가중치 크기 등에 패널티를 부여하는 방법
- 대표 방식
    1) L1 Regularization
        일부 가중치를 0으로 만듬 = 특정 Feature를 사용하지 않음
    2) L2 Regularization
        큰 가중치를 줄이는 방향으로 학습
        LogisticRegression의 기본 규제 방식
'''
# 21. solver
'''
- LogisticRegression에서 최적의 가중치를 찾는 알고리즘
- 대표적인 solver
    1) lbfgs : 일반적으로 많이 사용, L2 규제 지원
    2) liblinear : 작은 데이터셋에 적합, L1,L2 규제 지원
    3) saga : 대용량 데이터 셋에 적합, L1/L2 규제 지원
'''
'''
# normal (정상적인) <-> abnormal
- 기준 범위에서 벗어나지 않는 상태
- 암묵적으로 정상으로 인정하는 기준 범위가 있음
- 예) normal temperature, normal operation, normal blood pressure
- 예시) 직원이 정상적으로 출근했다

# regular (규칙적인, 정기적인) <-> irregular
- 일정한 패턴/주기/형식이 유지되는 상태
- 문맥에 따라 '통상적인, 보통의'라는 의미로도 사용
- 예) regular exercise, regular meeting, regular interval
- 예) regular size, regular customer, regular coffee
- 예시) 직원이 매일 오전 9시에 출근한다

# general (일반적인, 전반적인) <-> specific
- 특정 대상이나 상황에 한정되지 않고 넓은 범위에 적용되는 상태
- 예) general knowledge, general rule, general purpose
- 예) general public, general question
- 예시) 일반적으로 직원들은 오전 9시에 출근한다

# Normalization (정규화)
- 데이터의 범위를 맞춤 = 데이터를 정리
- normalize = 일정한 기준이나 범위에 맞추다
- 서로 다른 크기나 범위를 가진 데이터를 일정한 범위로 변환하는 전처리
- 데이터의 값 범위를 맞추어 특성 간 크기 차이를 줄이는 것이 목적
- 대표적인 방법: Min-Max Normalization
- 일반적으로 값을 0 ~ 1 범위로 변환
- 공식: (x - 최솟값) / (최댓값 - 최솟값)
- 예) 원본 점수 : 50, 60, 70, 80, 100,  정규화 결과 : 0.0, 0.2, 0.4, 0.6, 1.0
- 예시) 키가 150~190이고 연봉이 3천만~1억이라면
          두 특성의 숫자 크기가 매우 다르므로 비슷한 범위로 맞춰준다.

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_normalized = scaler.fit_transform(X)

# Regularization (규제)
- 모델의 복잡도를 제어 = 모델을 제어
- regularize = 지나치게 자유롭거나 복잡하지 않도록 규칙/제약을 부여
- 모델이 학습 데이터에 지나치게 맞춰지는 것을 막기 위해 제약을 추가하는 방법
- 모델의 가중치가 지나치게 커지는 것을 억제하여 과적합을 줄이는 것이 목적
- 대표적인 방법: L1, L2 Regularization
- L1 Regularization : 가중치의 절댓값에 패널티를 부여, 일부 가중치를 0으로 만들 수 있음, 
                              특성 선택 효과가 생길 수 있음
- L2 Regularization : 가중치의 제곱에 패널티를 부여, 큰 가중치를 줄이는 방향으로 학습,
                              , LogisticRegression 등에서 많이 사용
- 예시) 시험 문제 100개를 통째로 외우는 학생에게 
          "세부 답을 전부 외우지 말고 핵심 원리를 중심으로 공부해"라고 제한을 거는 것과 비슷

from sklearn.linear_model import LogisticRegression
model = LogisticRegression(
    # C : 규제 강도의 역수
    # C가 작음=규제가 강함=모델이 단순해 짐
    # C가 큽=규제가 약함 = 모델이 복잡해질 가능성이 커짐
    C=0.1, 
    max_iter=1000
)

# Generalization (일반화)
- 새로운 데이터에서도 잘 작동 = 모델의 최종 목표
- generalize = 특정 사례에서 학습한 내용을 일반적인 상황에도 적용
- 머신러닝 모델의 가장 중요한 목표 중 하나
- 학습 데이터에서 배운 패턴을 처음 보는 새로운 데이터에도 적용하는 능력
- 특정 학습 데이터에만 잘 맞는 것이 아니라 다양한 데이터에서 성능을 유지해야 함
- 예) 학습 정확도: 99%, 테스트 정확도: 70%
        - 학습 데이터에는 매우 잘 맞음
        - 새로운 데이터에서는 성능이 크게 하락
        - 과적합 가능성
        - 일반화 성능이 좋지 않음
- 예) 학습 정확도: 92%, 테스트 정확도: 90%
        - 학습 데이터와 새로운 데이터에서 비슷한 성능
        - 비교적 좋은 일반화 성능
- 예시) 교재의 문제를 그대로 외운 것이 아니라
          원리를 이해해서 처음 보는 응용문제도 풀 수 있는 상태

# 전체 흐름
데이터 > Normalization / Standardization > 학습 > Regularization > 과적합 감소 > Generalization 향상
'''









