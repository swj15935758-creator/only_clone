# day12_ex1.py
# 주제: 그룹핑, 집계, 정렬, 병합, 피벗테이블
from itertools import groupby

from python.print_util import pp
import pandas as pd

# 주문 정보 데이터 12행 7열 ) (12,7)
sales_data = {
    "order_id": ["O001", "O002", "O003", "O004", "O005", "O006", "O007", "O008", "O009", "O010", "O011", "O012"],
    "month": ["2026-01", "2026-01", "2026-01", "2026-01", "2026-02", "2026-02", "2026-02", "2026-02", "2026-03", "2026-03", "2026-03", "2026-03"],
    "department": ["D01", "D02", "D01", "D03", "D02", "D01", "D03", "D02", "D01", "D03", "D02", "D04"],
    "employee": ["서준", "지우", "민재", "서연", "지우", "서준", "서연", "하윤", "민재", "도윤", "하윤", "시우"],
    "product": ["노트북", "모니터", "키보드", "노트북", "마우스", "모니터", "키보드", "노트북", "마우스", "노트북", "모니터", "키보드"],
    "units": [2, 5, 10, 1, 12, 4, 8, 2, 15, 3, 6, 5],
    "unit_price": [1200000, 350000, 80000, 1200000, 45000, 350000, 80000, 1200000, 45000, 1200000, 350000, 80000]
}
# 딕셔너리 > 데이터프레임
df = pd.DataFrame(sales_data)
pp(df)
df.info()

# 매출액 계산
# 파생 컬럼(파생 변수) : 원본데이터에는 없지만 연산을 위해서 새로 생성한 컬럼(파생변수)
df['sales'] = df['units'] * df['unit_price'] # 매출 = 수량 * 단가
pp(df)
df.info()

# groupyby() 그룹핑
# groupyby(그룹할컬럼등)[집계할컬럼들].집계함수
dept_sales = df.groupby('department')['sales'].sum()
pp(type(groupby('department'))) #<class 'itertools.groupby'>
pp(dept_sales)
pp(type(dept_sales)) # <class 'pandas.Series'>


# as_index=False : 그룹핑기준을 인덱스로 사용하지 않음 = 인덱스 새로 생성
dept_sales = df.groupby('department', as_index=False)['sales'].sum()
pp(dept_sales)
pp(type(dept_sales)) # <class 'pandas.DataFrame'>

# 여러 컬럼 집계
dept_sales = df.groupby('department')[['sales','units']].sum() # 데이터 프레임
pp(dept_sales)

# agg()로 여러 집계
sales_stats = (df
               .groupby('department')['sales']
               .agg(['sum','mean','max','count']))
pp(sales_stats)

# Named Aggreation : 집계 결과를 변수에 저장
report = (
    df.groupby('department')
    .agg(
        total_sales=('sales','sum'),
        avg_sales=('sales','mean'),
        total_units=('units','sum'),
        order_count=('order_id','count'),
        employee_count=('employee','nunique'),
    )
    .reset_index()
)
pp(report)
# 매출 평균 값을 소수점 없이 정수로 변환
report['avg_sales'] = report['avg_sales'].round(0).astype(int)
pp(report)

# 2차 그룹핑
# month 로 그룹핑 하고 그룹핑한 각각의 month 에서 department로 그룹핑
monthly_dept = (
    df.groupby(['month','department'], as_index=False)
    .agg(
        total_sales=('sales','sum'),
        total_units=('units','sum'),
    )
)
pp(monthly_dept)

# sort_values() 값을 기준으로 오름차순(ascending)/내림차순 정렬(descending)
ranked = report.sort_values(
    # 정렬 기준 컬럼들 2차 정렬(total_sales 로 정렬한 후에 다시 total_units로정렬)
    by=['total_sales','total_units'],
    ascending=[False, True], # total_sales 에대해 내림차순, total_units에 대해 오름차순 정렬
    ignore_index=True # 기존 인덱스 무시하고 인덱스 재구성
)
ranked.index = ranked.index + 1 # 순위를 1부터 하기위해 인덱스에 1 더함
pp(ranked)

top3 = report.nlargest(3, 'total_sales') # 매출 상위 3개
pp(top3[['department','total_sales']])

# merge : 컬럼을 기준으로 데이터프레임 병합

# 부서 정보 데이터 프레임
dept_info = pd.DataFrame({
    "department": ["D01", "D02", "D03"],
    "department_name": ["플랫폼", "데이터", "서비스"],
    "manager": ["김서준", "박지우", "이서연"],
    "region": ["서울", "서울", "부산"]
})
pp(dept_info)

# inner merge : 양쪽에 모두 존재하는 부서만 병합
inner_result = report.merge(
    dept_info, #병합할 데이터 프레임
    on='department', # 키 컬럼
    how='inner', # 병합 방식
    validate='one_to_one' # 검증 방식
)
pp(inner_result)

# left merge : 왼쪽에 존재하는 모든 부서는 유지
left_result = report.merge(
    dept_info,
    on='department',
    how='left',
    # _merge
    # both : 양 쪽에 키가 모두 있음
    # left_only : 왼쪽에만 키가 있음
    # right_only : 오른쪽에만 키가 있음
    indicator = True, # _merged 생성
    validate='one_to_one'
)
pp(left_result)
# .value_counts() 값이 몇개가 있는지
pp(left_result['_merge'].value_counts())


# left merge : 왼쪽에 존재하는 모든 부서는 유지
right_result = report.merge(
    dept_info,
    on='department',
    how='right',
    indicator = True, # _merged 생성
    validate='one_to_one'
)
pp(right_result)

# 서로 키 컬럼영이 다른 경우
# dept_info 데이터프레임의 department 컬럼명을 변경한 데이터프레임 생성
dept_info2 = dept_info.rename(columns={'department':'dept_code'})
different_key_result = report.merge(
    dept_info2,
    left_on='department', # 왼쪽의 키컬럼명
    right_on='dept_code', # 오륹쪽의 키컬럼명
    how='left',
).drop(columns=['dept_code']) # dept_code 컬럼 제거
pp(different_key_result)

# pivot_table() : 분석 요약표 생성
pivot_sales = df.pivot_table(
    values='sales', # 집계 대상 컬럼
    index='month', # 행
    columns='department', # 열의 기준
    aggfunc='sum', # 집계 함수
    fill_value=0 # 결측치인 경우 0 으로 처리
)
pp(pivot_sales)

# 합계가 포함된 피벗 테이블
pivot_total = df.pivot_table(
    values='sales',  # 집계 대상 컬럼
    index='month',  # 행
    columns='department',  # 열의 기준
    aggfunc='sum',  # 집계 함수
    fill_value=0,  # 결측치인 경우 0 으로 처리
    margins = True, # 컬럼 추가 여부
    margins_name='Total'  # 추가되는 항목
)
pp(pivot_total)
pp(type(pivot_total)) # <class 'pandas.DataFrame'>

# 최종 실적표

raw_total = df['sales'].sum() # 원본 세일즈 합
report_total = report['total_sales'].sum() # 레포트 세일즈의 합
pivot_grand_total = pivot_total.loc['Total','Total']

final_report = (
    report.merge(
        dept_info,
        on='department',
        how='left',
        validate='one_to_one'
    ).sort_values(
        'total_sales',
        ascending=False,
        ignore_index=True
    )
)

final_report['sales_share_pct'] = (
    final_report['total_sales'] / final_report['total_sales'].sum() * 100
).round(1)

pp(final_report)






















