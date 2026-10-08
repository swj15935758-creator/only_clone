
# day16_challenge.py
# 주제:AI휴먼 16일차 Challenge 과제
# 주제: 산업 장비 고장 예측과 데이터누수 점검
#
# 다음 데이터는 산업 장비의 센서와 운영 기록입니다. 목표는 현재 시점의 정보로 failure_next_7d를 예측하는 것입니다.
#
# 컬럼
# temperature_c: 현재 장비 온도
# vibration_mm_s: 현재 진동 수치
# operating_hours: 누적 가동시간
# alarm_count_24h: 최근 24시간 알람 수
# repair_completed_after_failure: 고장 발생 이후 수리 완료 여부
# failure_next_7d: 향후 7일 이내 고장 여부(0/1)
import sklearn

from python.dataanalysis.day11.day11_ex import missing_by_column
from python.print_util import pp , pt, up
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.dummy import DummyRegressor , DummyClassifier
from sklearn.utils.multiclass import type_of_target
from sklearn.utils.validation import  check_X_y

# 데이터
temperature_c                 = [61, 73, 68, 84, 59, 88, 76, 64, 91, 70]
vibration_mm_s                = [2.1, 3.8, 2.9, 5.7, 1.9, 6.2, 4.4, 2.3, 6.8, 3.1]
operating_hours               = [1200, 2800, 1900, 5100, 900, 6200, 3500, 1500, 7100, 2400]
alarm_count_24h               = [0, 2, 1, 5, 0, 6, 3, 1, 7, 2]
repair_completed_after_failure= [0, 0, 0, 1, 0, 1, 0, 0, 1, 0]
failure_next_7d               = [0, 0, 0, 1, 0, 1, 1, 0, 1, 0]

# # 신규 장비
# temperature_c=79
# vibration_mm_s=4.9
# operating_hours=4200
# alarm_count_24h=4
# 신규 장비 1대 데이터 DataFrame
new_X = pd.DataFrame({
    'temperature_c': [79],
    'vibration_mm_s': [4.9],
    'operating_hours': [4200],
    'alarm_count_24h': [4],
})

pp(new_X)
# 요구사항
# 제공 데이터를 Pandas DataFrame으로 생성합니다.
# 기존 장비 데이터 DataFrame
df = pd.DataFrame({
    'temperature_c': temperature_c,
    'vibration_mm_s': vibration_mm_s,
    'operating_hours': operating_hours,
    'alarm_count_24h': alarm_count_24h,
    'repair_completed_after_failure': repair_completed_after_failure,
    'failure_next_7d': failure_next_7d,
})

pp(df)
# failure_next_7d를 TARGET으로 선언합니다.
TARGET = 'failure_next_7d'
# 모든 입력 후보 컬럼을 CANDIDATE_FEATURES로 선언합니다.
CANDIDATE_FEATURES = df.columns.to_list()
pp(CANDIDATE_FEATURES)
# 실제 예측 시점에 알 수 없는 데이터 누수 컬럼을 찾아 LEAKAGE_FEATURES 목록에 선언합니다.
LEAKAGE_FEATURES = ['repair_completed_after_failure']
# CANDIDATE_FEATURES에서 누수 컬럼을 제외해 최종 FEATURES를 생성합니다.
FEATURES = CANDIDATE_FEATURES.copy()
FEATURES.remove(TARGET)
for col in LEAKAGE_FEATURES:
    FEATURES.remove(col)
pp(FEATURES)
# 다음 조건을 검사하는 build_xy(df, feature_cols, target_col) 함수를 작성합니다.
# def build_xy(df, feature_cols, target_col):
#     try:
#         # Target이 Feature에 포함되어 있으면 ValueError 발생
#         if target_col in feature_cols:
#             pp('Target이 Feature에 포함되어 있으면 안 됩니다.')
#
#         # 요청한 컬럼이 DataFrame에 없으면 keyError 발생
#         X = df[feature_cols]
#         y = df[target_col]
#
#         # X 또는 y에 결측치가 있으면 keyError 발생
#         if X.isna().sum().sum() > 0 or y.isna().sum() > 0:
#             pp('X 또는 y에 결측치가 있으면 안 됩니다.')
#             raise ValueError
#         # 정상이라면 X와 y 반환
#         return X, y
#     except KeyError as e:
#         pp('요청한 컬럼이 DataFrame에 없습니다.',e)
#     except ValueError as e:
#         pp('X 또는 y에 문제가 있습니다.',e)

def build_xy(df, feature_cols, target_col):
    if target_col in feature_cols:
        raise ValueError('Target 컬럼은 Feature에 포함 할 수 없습니다.')
    required_cols = feature_cols + [target_col]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f'존재 하지 않은 컬럼{missing_cols}')
    X = df[feature_cols]
    y = df[target_col]
    if X.isna().any().any() or y.isna().any():
        raise ValueError('X 축또는 y 축 결측치가 잇습니다')
    return X, y

# build_xy()를 이용해 X와 y를 생성합니다.
X,y = build_xy(df,FEATURES,TARGET)
# type_of_target(y)와 check_X_y()를 이용해 Target 유형과 입력 구조를 확인합니다.
pp(type_of_target(y)) # binary


def cheked_ckeck_X_y(X,y):
    X_checked, y_checked = check_X_y(
        X, y, dtype="numeric"
    )
    return X_checked.shape, y_checked.shape
pp(cheked_ckeck_X_y(X,y)) # ((10, 4), (10,))
# X와 y의 shape, 최종 Feature 목록, 제외한 누수 컬럼을 출력합니다.
pp(X.shape)
pp(y.shape)
pp(FEATURES)
pp(LEAKAGE_FEATURES)
# 신규 장비 1건을 new_X DataFrame으로 만들고 학습용 X와 컬럼 순서가 같은지 확인합니다
pp(new_X.columns.to_list() == FEATURES) # True
# 왜 repair_completed_after_failure가 누수인지 한 문장으로 출력합니다.
pp('repair_completed_after_failure는 고장 발생 이후에 알 수 있는 정보이므로 현재 시점의 고장을 예측할 때 사용하면 데이터 누수가 발생합니다.')

