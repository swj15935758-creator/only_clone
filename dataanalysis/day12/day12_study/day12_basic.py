# day12_basic.py
# 주제: AI휴먼 Day 12 Basic 과제
# 주제: 도서관 대출 데이터 그룹 집계와 정렬
#
# 다음 도서 대출 데이터를 사용하여 대출 현황을 분석하십시오.
#
import pandas as pd
from python.print_util import pp

loan_data = {
    "loan_id": ["L001", "L002", "L003", "L004", "L005", "L006", "L007", "L008", "L009", "L010"],
    "branch": ["강남", "강남", "마포", "종로", "마포", "강남", "종로", "마포", "강남", "종로"],
    "category": ["IT", "경제", "IT", "문학", "경제", "IT", "IT", "문학", "문학", "경제"],
    "loan_days": [7, 14, 10, 21, 8, 12, 9, 18, 6, 15]
}
#
#
# 요구사항

# DataFrame을 생성하십시오.
df = pd.DataFrame(loan_data)
pp(df)
# 지점별 대출 건수와 평균 대출일수를 계산하십시오.
# 결과 컬럼명을 loan_count, avg_loan_days로 구성하십시오.

branch_report = (
    df.groupby('branch')
    .agg(
        loan_count=('loan_id', 'count'),
        avg_loan_days=('loan_days', 'mean')
    )
    .reset_index()
)

# 평균 대출일수는 소수점 첫째 자리까지 표시하십시오.
branch_report['avg_loan_days'] = branch_report['avg_loan_days'].round(1)
pp(branch_report)

# 대출 건수가 많은 지점부터 내림차순 정렬하십시오.
ranked = branch_report.sort_values(
    by='loan_count',
    ascending=False,
    ignore_index=True
)
pp(ranked)

# 카테고리별 대출 건수도 별도로 계산하고 대출 건수가 많은 순으로 출력하십시오.
category_report = (
    df.groupby('category')
    .agg(
        loan_count=('loan_id', 'count')
    )
    .reset_index()
)
category_report = category_report.sort_values(
    by='loan_count',
    ascending=False,
    ignore_index=True
)

pp(category_report)