# day9_application.py
# 주제:AI휴먼 9일차 Application 과제
# 주제: 2차원 배열과 axis를 활용한 매장 매출 분석
#
# [상황]
# 4개 매장의 5일간 매출액(만원)이 다음과 같이 주어졌습니다.
# 각 행은 매장 A~D, 각 열은 월~금 데이터를 의미합니다.
#
# 매장 A: 120, 135, 128, 142, 150
# 매장 B: 98, 105, 110, 115, 120
# 매장 C: 160, 155, 172, 168, 180
# 매장 D: 130, 125, 140, 138, 145
#
# [요구사항]
# 데이터를 4행 5열 NumPy 배열로 생성하세요.
# 배열의 shape와 전체 원소 개수를 출력하세요.
# 매장별 5일 평균 매출을 계산하세요.
# 요일별 4개 매장 전체 매출 합계를 계산하세요.
# 평균 매출이 가장 높은 매장의 인덱스를 np.argmax()로 찾으세요.
# 전체 매출 평균을 계산하세요.
# 전체 평균의 110% 이상인 매출값만 조건 인덱싱으로 추출하세요.
# 전체 평균의 110% 이상인 값의 위치를 np.where()로 찾아 행 인덱스와 열 인덱스를 출력하세요.
#
# [조건]
# 매장별 평균 계산에는 axis=1을 사용합니다.
# 요일별 합계 계산에는 axis=0을 사용합니다.
# 반복문 없이 NumPy 집계와 조건 인덱싱을 사용합니다.
import numpy as np

# (1)데이터를 4행 5열 NumPy 배열로 생성하세요.
maket_add_money = np.array([
    [120,135,128,142,150],  # A매장
    [98,105,110,115,120],   # B매장
    [160,155,172,168,180],  # C매장
    [130,125,140,138,145]   # D매장
])

# (2)배열의 shape와 전체 원소 개수를 출력하세요.
print('매장 데이터 행렬 모양', maket_add_money.shape)
print('매장별 원소수', maket_add_money.size)
# (3)매장별 5일 평균 매출을 계산하세요.
print('매장별 평균', maket_add_money.mean(axis=1))
# (4)요일별 4개 매장 전체 매출 합계를 계산하세요.
print('요일별 전체 매출 합', maket_add_money.sum(axis=0))
# (5)평균 매출이 가장 높은 매장의 인덱스를 np.argmax()로 찾으세요.
print('평균 매출이 가장 높은 매장 인덱스',np.argmax(maket_add_money.mean(axis=1)))
# (6)전체 매출 평균을 계산하세요.
print('전체 매출 평균', maket_add_money.mean())
# (7)전체 평균의 110% 이상인 매출값만 조건 인덱싱으로 추출하세요.
print('전체 평균 110% 이상인 값',maket_add_money[maket_add_money >= maket_add_money.mean() * 1.1])
# (8)전체 평균의 110% 이상인 값의 위치를 np.where()로 찾아 행 인덱스와 열 인덱스를 출력하세요.
new = maket_add_money >= maket_add_money.mean() * 1.1
row_index,colomn_index = np.where(new)
print('탁월한 마켓 행렬 위치', f'행위치{row_index},렬위치{colomn_index}')





