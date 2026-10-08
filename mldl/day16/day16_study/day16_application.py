# # day16_application.py
# AI휴먼 16일차 Application 과제
# 주제: 구독 서비스 해지 예측 데이터 구성
#
# 다음 데이터는 구독 서비스 이용자의 최근 활동 정보입니다.
#
# 컬럼
# login_days_30: 최근 30일 접속일수
# support_tickets: 최근 고객지원 문의 건수
# contract_months: 현재까지 계약 개월 수
# autopay: 자동결제 사용 여부(Y/N)
# churned: 다음 달 해지 여부(0=유지, 1=해지)
#
import sklearn
from python.print_util import pp , pt, up
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.dummy import DummyRegressor , DummyClassifier
from sklearn.utils.multiclass import type_of_target
from sklearn.utils.validation import  check_X_y

# 데이터
login_days_30   = [27, 5, 18, 2, 25, 8, 21, 4, 29, 11]
support_tickets = [0, 4, 1, 5, 0, 3, 1, 4, 0, 2]
contract_months = [18, 2, 10, 1, 24, 5, 15, 3, 30, 7]
autopay         = ["Y", "N", "Y", "N", "Y", "N", "Y", "N", "Y", "N"]
churned         = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]



# 요구사항
#
# 제공 데이터를 Pandas DataFrame으로 생성합니다.
df = pd.DataFrame({
    'login_days_30'   : [27, 5, 18, 2, 25, 8, 21, 4, 29, 11],
    'support_tickets' : [0, 4, 1, 5, 0, 3, 1, 4, 0, 2],
    'contract_months' : [18, 2, 10, 1, 24, 5, 15, 3, 30, 7],
    'autopay'         : ["Y", "N", "Y", "N", "Y", "N", "Y", "N", "Y", "N"],
    'churned'         : [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
})
# autopay의 Y를 1, N을 0으로 변환합니다.
df['autopay']=df['autopay'].replace({
    'Y': '1',
    'N': '0',
}).astype('int')
# login_days_30, support_tickets, contract_months, autopay를 Feature로 정의합니다.
FEATURES = ['login_days_30','support_tickets','contract_months','autopay']
# churned를 Label로 정의합니다.
TARGET = 'churned'
# FEATURES, TARGET 상수를 이용해 X와 y를 생성합니다.
X = df[FEATURES]
y = df[TARGET]
# type_of_target(y)로 Target 유형을 확인합니다.
pp(type_of_target(y)) # binary
# check_X_y(X, y, dtype="numeric")로 입력 구조를 검증합니다.
# 검증된 X와 y의 shape를 출력합니다.
def cheked_ckeck_X_y(X,y):
    X_checked, y_checked = check_X_y(
        X, y, dtype="numeric"
    )
    return X_checked.shape, y_checked.shape
pp(cheked_ckeck_X_y(X,y)) # ((10, 4), (10,))
# 아래 신규 이용자 1명의 추론용 DataFrame new_X를 만들고 학습용 X와 컬럼 순서가 같은지 확인합니다.
# 신규 이용자
# login_days_30=9
# support_tickets=2
# contract_months=6
# autopay="N"
new_X = pd.DataFrame({
    'login_days_30':[9],
    'support_tickets':[2],
    'contract_months':[6],
    'autopay':["N"]
})
new_X['autopay']=new_X['autopay'].map({
    'Y': 1,
    'N': 0,
})

pp(X.columns)
pp(new_X.columns)
pp(X.columns == new_X.columns)

# 이 문제가 회귀·분류·군집 중 어떤 유형인지 출력합니다.
pp('분류 문제이다 피쳐값인 4개의 데이터와 타겟 값인 한개의 데이터가 있고 0 인지 1 인지 두가지를 나눠서')
