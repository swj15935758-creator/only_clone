# day12_application.py
# 주제:AI휴먼 Day 12 Application 과제
# 주제: 채용 지원 데이터와 직무 정보 결합
#
# 다음 두 DataFrame용 데이터를 사용하십시오.
#
# 지원 데이터
import pandas as pd
from python.print_util import pp

apply_data = {
    "applicant_id": ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08"],
    "job_code": ["J01", "J02", "J01", "J03", "J02", "J04", "J03", "J01"],
    "result": ["합격", "불합격", "합격", "서류검토", "합격", "합격", "불합격", "불합격"],
    "score": [88, 72, 91, 81, 86, 90, 69, 77]
}
# 직무 정보
job_data = {
    "job_code": ["J01", "J02", "J03"],
    "job_name": ["백엔드", "데이터분석", "AI서비스"],
    "team": ["플랫폼", "데이터", "AI"]
}

# 요구사항
#
# 두 DataFrame을 생성하십시오.
df1 = pd.DataFrame(apply_data)
df2 = pd.DataFrame(job_data)

# 지원 데이터를 왼쪽 기준으로 직무 정보와 결합하십시오.
# indicator=True를 사용하여 결합 상태를 확인하십시오.
# 결합되지 않은 직무 코드가 무엇인지 출력하십시오.
left_result = pd.merge(
    df1,
    df2,
    on='job_code',
    how='left',
    indicator=True,
)
pp(left_result)

df3=left_result
# 직무명이 없는 행은 "미등록 직무"로 표시한 후 결과를 다시 출력하십시오
df3['job_name'] = df3['job_name'].fillna('미등록 직무')
pp(df3)

# 직무별 지원자 수, 평균 점수, 최고 점수를 Named Aggregation으로 계산하십시오.
report = (
    df3.groupby(['job_code','job_name'])
    .agg(
        total_applicant_count=('applicant_id', 'count'),
        total_mean_score=('score','mean'),
        total_best_score=('score','max'),
    )
    .reset_index()
)


# 평균 점수는 소수점 첫째 자리까지 표시하십시오.
report['total_mean_score']=report['total_mean_score'].round(1)
pp(report)

# 평균 점수가 높은 직무부터 정렬하십시오.
ranked = report.sort_values(
    by = 'total_mean_score',
    ascending = False,
)


pp(ranked)

""" [코드의 흐름]
DataFrame 생성
→ left merge
→ 없는 job_name 채우기
→ 직무별 groupby
→ agg로 지원자 수 / 평균 / 최고점수 계산
→ 평균 반올림
→ 평균 점수 기준 내림차순 정렬
→ 출력
"""
