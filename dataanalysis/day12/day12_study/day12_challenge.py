# day12_challenge.py
# 주제:주제: 온라인 학습 활동 피벗 분석
import pandas as pd
from python.print_util import pp

# 다음 온라인 학습 활동 데이터를 사용하십시오.
activity_data = {
    "activity_id": ["E01", "E02", "E03", "E04", "E05", "E06", "E07", "E08", "E09", "E10", "E11", "E12"],
    "month": ["2026-01", "2026-01", "2026-01", "2026-02", "2026-02", "2026-02", "2026-03", "2026-03", "2026-03", "2026-03", "2026-02", "2026-01"],
    "course": ["Python", "AI", "Cloud", "Python", "AI", "Cloud", "Python", "AI", "Cloud", "Python", "AI", "Cloud"],
    "learner": ["민준", "서연", "지우", "민준", "하윤", "지우", "도윤", "서연", "시우", "하윤", "민준", "도윤"],
    "study_minutes": [120, 95, 80, 150, 110, 90, 130, 125, 100, 75, 140, 105],
    "completed": [1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1]
}


# 과정 정보
course_data = {
    "course": ["Python", "AI", "Cloud"],
    "category": ["Programming", "AI", "Infrastructure"],
    "instructor": ["김강사", "이강사", "박강사"]
}
# 1. 데이터 프레임 생성
df_activity_data = pd.DataFrame(activity_data)
df_course_data = pd.DataFrame(course_data)
# 2. 데이터 결합
# 요구사항
# 활동 데이터와 과정 정보를 course 기준으로 결합하십시오.
course_dept_merge = pd.merge(
    df_activity_data,
    df_course_data,
    on="course",
    how="left"
)
# 3. 데이터 그루핑 및 집계
# 과정별 총 학습시간, 평균 학습시간, 활동 건수, 완료 건수를 계산하십시오.
course_group_data = (
    course_dept_merge.groupby("course")
    .agg(
        total_study = ("study_minutes", "sum"),
        avg_study = ("study_minutes", "mean"),
        activity_count = ("learner", "count"),
        complete_count = ("completed", "sum"),
    )
)
pp(course_group_data)
# 과정별 완료율(%)을 완료 건수 / 활동 건수 * 100으로 계산하고 소수점 첫째 자리까지 표시하십시오.
course_group_data['complete_rate'] = (
    course_group_data['complete_count'] / course_group_data['activity_count']*100
).round(1)
# 완료율이 높은 과정부터 정렬하십시오.
course_group_df = course_group_data.sort_values(
    by='complete_rate',
    ascending=False
)
pp(course_group_data)
# 월을 행, 과정을 열로 하고 study_minutes의 합계를 값으로 하는 피벗 테이블을 만드십시오.
# 피벗 테이블의 빈 값은 0으로 표시하고 전체 합계를 추가하십시오.
pivot_month_course_df = course_dept_merge.pivot_table(
    values='study_minutes',
    index='month',
    columns='course',
    fill_value=0,       # 결측치인 경우 0으로 처리
    aggfunc='sum',
    margins=True,       # 전체 합계 행/열 생성
    margins_name='Total'
)
pp(pivot_month_course_df)
# 월을 행, 과정 카테고리를 열로 하고 completed의 평균을 값으로 하는 두 번째 피벗 테이블을 만드십시오.
# 두 번째 피벗 테이블의 평균값을 완료율(%)로 변환해 소수점 첫째 자리까지 표시하십시오.
pivot_month_category_df = course_dept_merge.pivot_table(
    values='completed',
    index='month',
    columns='category',
    fill_value=0,
    aggfunc='mean'
)
pivot_month_category_df = (pivot_month_category_df * 100).round(1)
pp(pivot_month_category_df)

# 원본 study_minutes 총합과 첫 번째 피벗 테이블의 전체 합계가 같은지 검증하십시오.
original_total = course_dept_merge['study_minutes'].sum()
pivot_total = pivot_month_course_df.loc['Total', 'Total']

pp(original_total)
pp(pivot_total)
pp(original_total == pivot_total)