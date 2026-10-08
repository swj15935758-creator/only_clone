# day15_application.py
# 주제:day15 Application 과제 - 온라인 쇼핑 반품 데이터 EDA
# [상황]
# day15_application_data.csv에는 온라인 쇼핑 주문의 반품 여부와 고객·상품 정보가 저장되어 있습니다. 일부 금액과 수량 값은 잘못된 문자열 또는 결측 상태이며 반품사유 표기가 일관되지 않습니다.
from itertools import groupby

from python.print_util import pp
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# 그래프 기본 설정
sns.set_theme(style="whitegrid")
# 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic' # Windows: 나눔고딕
elif os_name == "Darwin":
    plt.rcParams["font.family"] = "AppleGothic"    # macOS: 애플고딕
elif os_name == "Linux":
    plt.rcParams["font.family"] = "NanumGothic"    # Linux: 나눔고딕

# [상황]
# day15_basic_data.csv에는 공공도서관의 도서 대출 기록이 저장되어 있습니다.
# 일부 값에는 공백, 표기 불일치, 결측치와 중복이 포함되어 있습니다.

# 경로
BASE_DIR = Path(__file__).parent # 현재 경로의 상위 경로
DATA_FILE = BASE_DIR /'..'/ 'assets' / 'day15_application_data.csv' # CSV 파일 경로
OUTPUT_DIR = Path(__file__).with_name('day15_ouput') # 결과 파일 저장 디렉토리
OUTPUT_DIR.mkdir(exist_ok=True)
# [요구사항]
# 데이터 구조와 품질을 점검하고 발견한 문제를 코드 출력으로 확인하세요.
df = pd.read_csv(DATA_FILE,encoding='utf-8-sig')
pp('(행,열) :',df.shape)
pp('자료형 :',df.dtypes)
pp('결측치 개수 :',df.isna().sum())
pp('중복건수: ',df.duplicated().sum())
# pp(df)

# 주문일을 datetime으로, 주문금액과 수량을 수치형으로 변환하세요.
clean_df = df.copy()
clean_df['주문일']= pd.to_datetime(clean_df['주문일'],errors='coerce')
clean_df['주문금액'] = pd.to_numeric(clean_df['주문금액'],errors='coerce')
clean_df['수량'] = pd.to_numeric(clean_df['수량'],errors='coerce')
# 반품여부 값을 Y/N 두 값으로 통일하세요.
clean_df['반품여부'] = clean_df['반품여부'].replace({
    '정상': 'N',
    'NO': 'N',
    'no': 'N',
    '반품': 'Y',
    'yes': 'Y',
    'YES': 'Y',
})
# 반품사유의 size, 사이즈, SIZE를 사이즈로 통일하고 반품이
# 아닌 행의 반품사유 결측치는 해당없음으로 처리하세요.
clean_df['반품사유'] = clean_df['반품사유'].replace({
    'size': '사이즈',
    '사이즈': '사이즈',
    'SIZE': '사이즈',
})
not_returned = clean_df['반품여부'].eq('N')
reason_missing = clean_df['반품사유'].isna()
clean_df.loc[not_returned & reason_missing, '반품사유'] = '해당없음'
# pp(clean_df['반품사유'])

# 주문금액이 0 이하이거나 수량이 0 이하인 값은 결측 처리한 뒤 각 컬럼의 중앙값으로 대체하세요.
invalid_amount = clean_df['주문금액'].le(0) # 0이하
clean_df.loc[invalid_amount, '주문금액'] = pd.NA #  loc 조건으로 0이하 대체
amount_median = clean_df['주문금액'].median() # 중앙값
clean_df['주문금액'] = clean_df['주문금액'].fillna(amount_median) # 중앙값 대체

invalid_quantity = clean_df['수량'].le(0) # 0이하
clean_df.loc[invalid_quantity, '수량'] = pd.NA #  loc 조건으로 0이하 대체
quantity_median = clean_df['수량'].median() # 중앙값
clean_df['수량'] = clean_df['수량'].fillna(quantity_median) # 중앙값 대체

# 주문ID 기준 중복은 마지막 행을 유지하세요.
clean_df = clean_df.drop_duplicates(subset='주문ID', keep='last').reset_index(drop=True)
pp(df)
pp(clean_df)
# 다음 KPI를 계산하세요.
pp('[KPI]')

# 유효 주문 건수
total_inquiries = len(clean_df)

# 전체 주문금액 합계
total_amount = clean_df['주문금액'].sum()

# 반품률
return_rate = clean_df['반품여부'].eq('Y').mean() * 100

# 반품 주문의 평균 주문금액
return_amount_isY = clean_df['반품여부'].eq('Y')
return_amount_avg = clean_df.loc[return_amount_isY, '주문금액'].mean()

pp(f'유효 주문 건수: {total_inquiries}건')
pp(f'전체 주문금액 합계: {total_amount}원')
pp(f'반품률: {return_rate:.1f}%')
pp(f'반품 주문의 평균 주문금액: {return_amount_avg:.1f}원')


# 카테고리별 주문 건수·주문금액 합계·반품률을 하나의 요약표로 작성하세요.
clean_df['반품여부_bool'] = clean_df['반품여부'].eq('Y')

category_summary = (
    clean_df.groupby('카테고리')
    .agg(
        주문건수=('주문ID', 'count'),
        주문금액합계=('주문금액', 'sum'),
        반품률=('반품여부_bool', 'mean')
    )
)

category_summary['반품률'] = category_summary['반품률'] * 100


# 반품률이 높은 카테고리 순으로 정렬하세요.
category_summary = category_summary.sort_values(
    '반품률',
    ascending=False
)

pp(category_summary)


# 카테고리별 반품률 막대그래프
fig,ax = plt.subplots(figsize=(8,5))
sns.barplot(
    data=category_summary.reset_index(),
    x='카테고리',
    y='반품률',
    ax=ax,
)

plt.title('카테고리별 반품률')
plt.xlabel('카테고리')
plt.ylabel('반품률(%)')
plt.show()


# 반품사유별 건수 막대그래프
return_reason_count = (
    clean_df.loc[clean_df['반품여부'].eq('Y'), '반품사유']
    .value_counts()
)

sns.barplot(
    x=return_reason_count.index,
    y=return_reason_count.values
)

plt.title('반품사유별 건수')
plt.xlabel('반품사유')
plt.ylabel('건수')
plt.show()


# 주문금액 분포 히스토그램
fig,ax = plt.subplots(figsize=(8,5))
sns.histplot(
    data=clean_df,
    x='주문금액',
    bins=8,
    kde=True,
    ax=ax,
)

plt.title('주문금액 분포')
plt.xlabel('주문금액')
plt.ylabel('건수')
plt.show()
# 결과를 근거로 5줄 인사이트와 추가로 확인해야 할 데이터 2개를 출력하세요.

# 결과를 근거로 5줄 인사이트와 추가로 확인해야 할 데이터 2개를 출력하세요.

pp('[인사이트]')
pp('1. 전체 유효 주문 20건 중 반품 주문은 9건으로, 전체 반품률은 45.0%입니다.')
pp('2. 의류 카테고리의 반품률은 약 83.3%로 전체 카테고리 중 가장 높습니다.')
pp('3. 전자기기의 반품률은 40.0%, 식품은 25.0%, 생활용품은 20.0%로 나타났습니다.')
pp('4. 반품사유 중 사이즈가 4건으로 가장 많아, 의류의 높은 반품률과 함께 추가 확인이 필요합니다.')
pp('5. 반품 주문의 평균 주문금액은 약 165,000원으로, 고액 주문과 반품의 관계도 추가 분석할 필요가 있습니다.')

pp('[추가로 확인해야 할 데이터]')
pp('1. 상품별 상세 정보: 어떤 상품에서 사이즈·불량 등의 반품이 집중되는지 확인할 필요가 있습니다.')
pp('2. 고객별 구매 이력: 특정 고객이나 고객등급에서 반복적인 반품이 발생하는지 확인할 필요가 있습니다.')