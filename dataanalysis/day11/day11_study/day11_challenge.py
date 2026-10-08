# # day11_challenge.py
# AI휴먼 11일차 Challenge 과제
# 주제: 온라인 주문 데이터 품질 점검과 전처리 근거 기록

from python.print_util import pp
import pandas as pd

sample_data = {
    '주문ID': ['O2001', 'O2002', 'O2003', 'O2004', 'O2005', 'O2002', 'O2006', 'O2007', 'O2008'],
    '상품분류': ['노트북', '마우스', '키보드', '모니터', '헤드셋', '마우스', '웹캠', '노트북', '마우스'],
    '수량': ['1', '2', 'unknown', '1', '2', '2', '', '1', '3'],
    '결제금액': ['1200000', '44000', '65000', '350000', '오류', '44000', '98000', '1350000', '66000'],
    '채널': ['웹', '앱', '앱', '', '웹', '앱', '앱', '웹', '앱'],
    '고객등급': ['Gold', 'Silver', 'Silver', 'Gold', '', 'Silver', 'Bronze', 'Gold', 'Silver']
}


# 요구사항
#
# 아래 데이터를 day11_orders_raw.csv로 생성하고 Pandas로 읽으십시오.

# 원본 데이터 저장
sample_data = pd.DataFrame(sample_data) # 딕셔너리 > 데이터 프레임

# 데이터 프레임 > csv
sample_data.to_csv('day11_orders_raw.csv',index=False,encoding='utf-8-sig')

df = pd.read_csv('day11_orders_raw.csv',encoding='utf-8-sig') # 원본

s_df = pd.read_csv('day11_orders_raw.csv',encoding='utf-8-sig') # 샘플 바꾸는 데이터


# 전처리 전의 행 수, 전체 결측치 수, 중복 행 수, 컬럼별 dtype을 확인하십시오.

before_all_column = df.shape[0] # 전 전체행
before_all_rufcmr = df.isna().sum().sum() # 전 결측치 전체
before_dul = df.duplicated(subset=['주문ID']).sum() # 전 중복 주문ID

pp('전처리 전 행 수:', before_all_column)
pp('전처리 전 전체 결측치:', before_all_rufcmr)
pp('전처리 전 중복 주문ID:', before_dul)
pp('전처리 전 dtype:\n', df.dtypes)


# loc를 이용해 채널이 "앱"인 주문의 주문ID, 수량, 결제금액을 조회하십시오.

app_order = s_df.loc[s_df['채널'] == '앱',['주문ID','수량','결제금액']]

pp('[앱 주문]\n', app_order)


# iloc를 이용해 앞 5행과 앞 4열을 조회하십시오.

pt_order = s_df.iloc[0:5, 0:4]
pp(pt_order)


# 수량과 결제금액을 pd.to_numeric(errors="coerce")로 변환하십시오.

s_df['수량'] = pd.to_numeric(s_df['수량'],errors='coerce')

s_df['결제금액'] = pd.to_numeric(s_df['결제금액'],errors='coerce')


# 숫자 변환 직후 새로 발생한 결측치를 다시 확인하십시오.

pp('수량 결측치:', s_df['수량'].isna().sum())
pp('결제금액 결측치:', s_df['결제금액'].isna().sum())


# 수량의 결측치는 중앙값으로 대체하십시오.

amount_median = s_df['수량'].median()

s_df['수량'] = s_df['수량'].fillna(amount_median)

pp(s_df['수량'])


# 결제금액의 결측치는 중앙값으로 대체하십시오.

price_median = s_df['결제금액'].median()

s_df['결제금액'] = s_df['결제금액'].fillna(price_median)

pp(s_df['결제금액'])


# 채널의 결측치는 "미확인"으로 대체하십시오.

s_df['채널'] = s_df['채널'].fillna('미확인')
pp(s_df['채널'])


# 고객등급의 결측치는 최빈값으로 대체하십시오.

min_customer = s_df['고객등급'].mode()[0]

s_df['고객등급'] = s_df['고객등급'].fillna(min_customer)

pp(s_df['고객등급'])


# 주문ID를 기준으로 중복을 확인하고 첫 번째 주문만 유지하십시오.

order_dul = s_df.duplicated(subset=['주문ID']).sum()

pp('주문ID 중복 개수:', order_dul)

s_df = s_df.drop_duplicates(subset=['주문ID'],keep='first')


# Index를 다시 정리하십시오.

s_df = s_df.reset_index(drop=True)
pp(s_df)


# 수량과 결제금액을 정수형으로 변환하십시오.

s_df['수량'] = s_df['수량'].astype('int64')
s_df['결제금액'] = s_df['결제금액'].astype('int64')


# 결제금액이 50,000원 이상인 주문을 loc로 조회하십시오.

over_dhaks = s_df.loc[s_df['결제금액'] >= 50_000]

pp(over_dhaks)


# 다음 컬럼을 가진 전처리 근거 DataFrame을 작성하십시오.
# 항목 / 발견문제 / 처리방법 / 처리근거

reason_df = pd.DataFrame({
    '항목': ['수량', '결제금액', '채널', '주문ID 중복'],
    '발견문제': [
        'unknown 및 결측치',
        '오류값 포함',
        '결측치 존재',
        '같은 주문ID 존재'
    ],
    '처리방법': [
        '숫자형 변환 후 중앙값 대체',
        '숫자형 변환 후 중앙값 대체',
        '미확인으로 대체',
        '첫 번째 주문만 유지'
    ],
    '처리근거': [
        '숫자 분석을 위해 변환 후 결측값 보완',
        '오류값을 NaN으로 바꾼 뒤 중앙값으로 보완',
        '채널 정보가 없는 상태를 표시',
        '중복 주문 제거'
    ]
})

pp(reason_df)


# 전처리 전후 비교 DataFrame을 작성하십시오.
#
# 점검항목 / 전처리전 / 전처리후
# 행 수
# 전체 결측치
# 중복 주문ID

after_all_column = s_df.shape[0] # 후 전체행
after_all_rufcmr = s_df.isna().sum().sum() # 후 결측치 전체
after_dul = s_df.duplicated(subset=['주문ID']).sum() # 후 중복 주문ID

comparison_df = pd.DataFrame({
    '점검항목': ['행 수', '전체 결측치', '중복 주문ID'],
    '전처리전': [before_all_column,before_all_rufcmr,before_dul],
    '전처리후': [after_all_column,after_all_rufcmr,after_dul]})

pp(comparison_df)


# 결제금액에 대해 전처리 후 count, mean, min, max를 출력하십시오.

pp(s_df['결제금액'].agg(['count', 'mean', 'min', 'max']))


# 정제된 데이터를 day11_orders_clean.csv로 저장하십시오.

s_df.to_csv('day11_orders_clean.csv',index=False,encoding='utf-8-sig')