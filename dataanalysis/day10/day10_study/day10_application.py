# Day 10 Application 과제 - 온라인 주문 데이터 기초 탐색
# 예상 수행시간: 35분
#
# [상황]
# 온라인 쇼핑몰의 최근 주문 내역을 전달받았습니다. 본격적인 매출 분석 전에 데이터 구조, 주문 금액의 분포, 주문 채널 구성을 확인하려고 합니다.
#
# [데이터]
# 아래 데이터를 코드에서 DataFrame으로 만든 뒤 online_orders.csv로 저장하여 사용하십시오.
#
# 주문번호,채널,상품분류,수량,주문금액
# O001,모바일,전자기기,1,120000
# O002,웹,생활용품,3,45000
# O003,모바일,패션,2,78000
# O004,웹,전자기기,1,210000
# O005,모바일,생활용품,5,65000
# O006,앱,패션,1,52000
# O007,앱,전자기기,2,330000
# O008,웹,패션,3,99000
#
# [문제]
# online_orders.csv를 DataFrame으로 읽으십시오.
# DataFrame의 타입과 전체 데이터를 출력하십시오.
# shape, ndim, size를 각각 출력하십시오.
# columns와 dtypes를 출력하십시오.
# 주문번호, 상품분류, 주문금액 3개 컬럼만 선택한 DataFrame을 만들어 출력하십시오.
# 주문금액 한 컬럼을 Series로 선택하고 객체 타입을 출력하십시오.
# 주문금액 Series의 합계, 평균, 중앙값, 최솟값, 최댓값을 출력하십시오.
# describe()로 숫자형 컬럼의 기초통계를 출력하십시오.
# 채널별 주문 건수를 value_counts()로 출력하십시오.
# 상품분류의 고유값 목록과 고유값 개수를 출력하십시오.
# pd.read_csv()의 usecols를 사용하여 채널과 주문금액만 다시 읽은 DataFrame을 출력하십시오.
# 분석 시작 전에 확인한 내용을 3줄의 출력 메시지로 요약하십시오. 예: 데이터 크기, 주문금액 평균, 가장 많이 사용된 채널
#
# [제출 조건]
# 조건 필터링이나 결측치 처리 없이 Day 10 범위의 기능만으로 해결할 것
# 각 단계가 무엇을 점검하는지 주석을 포함할 것
# day10_application.py

import pandas as pd

# 온라인 주문데이터 딕셔너리
order_data = { # 8 X 5
    "주문번호": ["O001", "O002", "O003", "O004", "O005", "O006", "O007", "O008"],
    "채널": ["모바일", "웹", "모바일", "웹", "모바일", "앱", "앱", "웹"],
    "상품분류": ["전자기기", "생활용품", "패션", "전자기기", "생활용품", "패션", "전자기기", "패션"],
    "수량": [1, 3, 2, 1, 5, 1, 2, 3],
    "주문금액": [120000, 45000, 78000, 210000, 65000, 52000, 330000, 99000],
}

# 딕셔너리 > 데이터프레임
source_df = pd.DataFrame(order_data)

# 데이터프레임 > CSV 파일
source_df.to_csv('online_orders.csv', index=False, encoding='utf-8-sig')

# CSV 파일 > 데이터프레임
orders_df = pd.read_csv('online_orders.csv', encoding='utf-8-sig')

print(type(orders_df)) # <class 'pandas.DataFrame'>

print(orders_df)

print('shape: ', orders_df.shape) # (8, 5)

print('ndim: ', orders_df.ndim) # 2

print('size: ', orders_df.size) # 40

print('columns: ', list(orders_df.columns)) # 컬럼 리스트

print(orders_df.dtypes) # 각 컬럼 데이터 타입

# 3개 컬럼 추출한 데이터프레임
selected_df = orders_df[['주문번호', '상품분류', '주문금액']]
print(selected_df)

# 주문금액 Series
amount = orders_df['주문금액']
print(type(amount)) # <class 'pandas.Series'>

print('합계: ', amount.sum())
print('평균: ', amount.mean())
print('중앙값: ', amount.median())
print('최대: ', amount.max())
print('최소: ', amount.min())

print(orders_df.describe()) # 기초 통계

# 채널별 주문 건수
print(orders_df['채널'].value_counts())

# 상품분류 고유값 목록
print('고유값: ', orders_df['상품분류'].unique())

# 상품분류 고유값 개수
print('고유값 개수: ', orders_df['상품분류'].nunique())

# 채널, 주문금액 2개 컬럼의 데이터 프레임
channel_amount_df = pd.read_csv(
    'online_orders.csv',
    encoding='utf-8-sig',
    usecols=['채널', '주문금액']
)
print(channel_amount_df)

# 가장 많이 사용된 채널의 이름
# print(orders_df['채널'].value_counts())
top_channel = orders_df['채널'].value_counts().index[0]

# 데이터 크기를 한 줄로 요약해 출력
print(f'데이터는 {orders_df.shape[0]}행, {orders_df.shape[1]}열 입니다.')

# 주문금액 평균을 한 줄로 요약해 출력
# ,.0f : 숫자 3자리마다 콤마, 소수점 이하 없는 실수
print(f'평균 주문금액은 {amount.mean():,.0f}원 입니다.')

# 가장 많이 사용된 채널을 한 줄로 요약해 출력
print(f'가장 많이 사용된 주문 채널은 {top_channel}입니다.')








