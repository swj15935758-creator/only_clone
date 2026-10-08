# day19_cls_metrics.py
# 분류 모델의 성능 평가 지표

from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score,recall_score,f1_score
)
from print_util import pp

# 상황 : 제품 100개를 정상 제품과 불량 제품으로 분류 하는 모델 (목적 : 불량 예측)
#       0 : 정상(Negative), 1 : 불량(Positive)
#       실제 정상 제품 80개, 실제 불량 제품 20개

# 예측결과
# - 실제 정상 80개 : 모델은 75개 정상이라고 예측, 5개 불량이라고 예측
# - 실제 불량 20개 : 모델은 4개 정상이라고 예측, 16개 불량이라고 예측

y_true = [0] * 80 + [1] * 20 # 실제 데이터
pp(y_true)
y_pred = [0] * 75 + [1] * 5 + [0] * 4 + [1] * 16 # 예측 데이터
pp(y_pred)

# 1. 혼동 행렬(Confusion Matrix)
# : 실제 값과 모델의 예측값을 비교해서 분류 모델이 어떻게 예측했는지 표 형태로 나타낸것
# : [[TN,FP]
# :  [FN,TP]]
# TN(True Negative) : 모델이 정상으로 예측 > 실제 정상 (맞춤)
# FP(False Positive) : 모델이 불량으로 예측 > 실제 정상 (틀림)
# FN(False Negative) : 모델이 정상으로 예측 > 실제 불량 (틀림)
# TP(True Positive) : 모델이 불량으로 예측 > 실제 불량 (맞춤)

cm=confusion_matrix(y_true, y_pred)
pp('1. 혼동 행렬')
pp(cm)

# 2차원 배열을 1차원 변환후 변수에 나눠 저장
TN,FP,FN,TP = cm.ravel() # 75 5 4 16
pp(TN,FP,FN,TP)

# 2. 정확도 (Accuracy)
# - 전체 데이터 중에서 모델이 올바르게 예측한 데이터의 비율
# - 맞게 예측한 경우 : TP + TN
# - 전체 데이터 : TP + FN + FP + FN
# - Accuracy : TP + TN / TP + TN + FP + FN
# - 샘플 데이터 : 75 + 16 / 75 + 16 + 4 + 5 = 0.91 = 91%

accuracy = accuracy_score(y_true,y_pred)
pp('2. 정확도')
pp(f'정확도: {accuracy * 100 :.1f}%')

# 정확도가 높다고 해서 항상 좋은 분류 모델이라고 할 수는 없음
# 예) 정상: 990개, 불량 10개
#       모델이 무조건 정상이라고 예측을 하면 990 / 1000 = 99%
#       정확도는 99%지만 실제 불량 10개를 하나도 찾지 못함
#       이렇게 클래스가 불균형한 데이터(Imbalanced Data) 에서는
#       정확도 만으로 모델을 평가 하기 힘듬

# 3. 정밀도 (Precision)
# : 모델이 불량(Positive)이라고 예측한 것 중에서 실제로 불량인 비율, 예측 우선
# : TP = 실제 불량, FP = 실제 정상
# : 정밀도 = TP / TP + FP
# : 샘플데이터 = 16 / 16 + 5 = 0.762 =76.2%

precision = precision_score(y_true,y_pred)
pp('3. 정밀도')
pp(f'정밀도 : { precision * 100 :.1f}%')

# 4. 재현율 (Recall)
# : 실제 불량(Positive)인 것 중에서 모델이 불량이라고 찾아낸 비율, 실제우선
# TP: 불량으로 예측했는데 불량, FN: 정상으로 예측했는데 불량
# : recall = TP / TP + FN
# : 샘플데이터 = 16 / 16 + 4 = 0.8 = 80%
recall = recall_score(y_true,y_pred)
pp('4. 재현율')
pp(f'재현율 : {recall * 100 :.1f}%')

# 5. 산술평균, 조화평균
# 1) 산술평균 (Arithmetic Mean)
# - 모든 값을 더한 후 값의 개수로 나눈 평균
# 식 : x1 + x2 + ... + xn  /  n

# 2) 조화평균 (Harmonic Mean)
# - 모든 값의 역수를 구한 후 역수들의 산술평균을 다시 역수로 만든 평균
# - 평균을 구할때 작은 값의 영향을 크게 받게 하기 위해 조화평균을 사용
# - 평균에 참여한 여러 값 중 작은 값의 영향을 높이기 위함
# - f1-score는 조화 평균을 사용해 Precision과 Recall의 균형을 표현
# - 좋은 모델이라면 Precision 과 Recall 이 균형 적이어야 하므로 조화평균을 사용함
# 식 : n  /  1/x1 + 1/x2 + ... 1/xn

# x1 = 80, x2 =20 이라고 할때
# 산술 평균 = (80 + 20) / 2 = 50
# 조회 평균 = 2 / (1/80 + 1/20) =32

# 6. f1-score
# - Precision 과 Recall의 조화평균
# - 둘 중 어느 한 쪽만 높은 모델이 좋은 점수를 받지 못하도록 두 지표의 균형을 평가하는 값
# - 식 : 2 / ((1/precision) + (1/recall)) => 2 * Precision * Recall / (Precision + Recall)
f1 = f1_score(y_true,y_pred)

pp('6. f1-score')
pp(f'f1-score : {f1 * 100 :.1f}%')







