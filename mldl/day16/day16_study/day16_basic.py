# day16_basic.pyAI휴먼 16일차 Basic 과제
# 주제: 택배 배송시간 예측 문제 정의
#
# 다음 데이터는 택배 배송 건별 정보입니다.
#
# 컬럼
# distance_km: 배송 거리(km)
# package_count: 배송 물품 수
# traffic_index: 교통 혼잡도(1~10)
# rain_mm: 강수량(mm)
# delivery_minutes: 실제 배송시간(분)
#


import sklearn
from python.print_util import pp , pt, up
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.dummy import DummyRegressor , DummyClassifier
from sklearn.utils.multiclass import type_of_target
from sklearn.utils.validation import  check_X_y


# 데이터
distance_km = [2.5, 4.1, 6.8, 3.2, 10.5, 8.7, 5.4, 12.1]
package_count    = [1, 3, 2, 1, 5, 4, 2, 6]
traffic_index    = [3, 6, 8, 4, 9, 7, 5, 10]
rain_mm          = [0, 0, 4, 12, 0, 7, 1, 15]
delivery_minutes = [18.5, 29.2, 46.8, 35.1, 61.4, 58.7, 34.6, 79.3]
RANDOM_STATE = 42
# 요구사항
# 아래 데이터를 Pandas DataFrame으로 생성합니다.
df = pd.DataFrame({
    'distance_km': distance_km,
    'package_count':package_count,
    'traffic_index' :traffic_index ,
    'rain_mm' : rain_mm,
    'delivery_minutes': delivery_minutes,
})
# distance_km, package_count, traffic_index, rain_mm를 Feature로 정의합니다.
FEATURES =['distance_km','package_count','traffic_index','rain_mm']
# delivery_minutes를 Label로 정의합니다.
TARGET = 'delivery_minutes'
# Feature 목록은 FEATURES, Label 컬럼명은 TARGET 상수로 선언합니다.
X = df[FEATURES]
y = df[TARGET]
X = df[FEATURES]
# X와 y를 생성하고 각각의 shape를 출력합니다.
pp(X.shape, y.shape) # (8, 4) (8,)
# X의 컬럼명과 y의 이름을 출력합니다.
pp(X.columns)
pp(y.name)

# type_of_target(y) 결과를 출력합니다.
pp(type_of_target(y)) # continuous
# 이 문제가 회귀·분류·군집 중 어떤 유형인지 출력하고 이유를 한 문장으로 출력합니다.
print('회귀 : 피쳐와 타겟을 통해 분석하고 연속된 값을 출력하기 떄문에'
      '애초에 배달시간과 거리,포장시간, 교통의 관계를 분석하기 떄문에')