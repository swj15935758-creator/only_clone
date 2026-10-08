import pandas as pd
from python.print_util import pp




# 다음 온라인 학습 활동 데이터를 사용하십시오.(12,6)
activity_data = {
    "activity_id": ["E01", "E02", "E03", "E04", "E05", "E06", "E07", "E08", "E09", "E10", "E11", "E12"],
    "month": ["2026-01", "2026-01", "2026-01", "2026-02", "2026-02", "2026-02", "2026-03", "2026-03", "2026-03", "2026-03", "2026-02", "2026-01"],
    "course": ["Python", "AI", "Cloud", "Python", "AI", "Cloud", "Python", "AI", "Cloud", "Python", "AI", "Cloud"],
    "learner": ["민준", "서연", "지우", "민준", "하윤", "지우", "도윤", "서연", "시우", "하윤", "민준", "도윤"],
    "study_minutes": [120, 95, 80, 150, 110, 90, 130, 125, 100, 75, 140, 105],
    "completed": [1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1]
}


# 과정 정보
course_data = { # (3,3)
    "course": ["Python", "AI", "Cloud"],
    "category": ["Programming", "AI", "Infrastructure"],
    "instructor": ["김강사", "이강사", "박강사"]
}
# 1. 데이터 프레임 생성
activity_df = pd.DataFrame(activity_data)
course_df = pd.DataFrame(course_data)
# activity_df.info()
# course_df.info()

# 2. 과정데이터, 활동 데이터 결합

merged = activity_df.merge(
    course_df, # 결합할 데이터 프레임
    on="course", # 키컬럼
    how="left", # 결합 방식 : 왼쪽
    validate="many_to_one" # 왼쪽에는  키값이 여러개, 오른쪽은 하나로 검증
)
# pp(merged)

# 3. 과정별 학습 활동 집계
course_summary = (
    merged.groupby('course')
    .agg(
        total_minutes=('study_minutes', 'sum'), # 전체 분 수
        avg_minutes=('study_minutes', 'mean'), # 학습 평균
        activity_count=('activity_id', 'count'), # 활동 횟수
        completed_count=('completed', 'count') # 완료 된 수
    ).reset_index() #인덱스 갱신
)
# pp(course_summary)

course_summary['avg_minutes']=course_summary['avg_minutes'].round(1) # 평균분수
course_summary['completion_rate_pct'] = ( # 완료율
    (course_summary['completed_count'] / course_summary['completed_count']) * 100
).round(1)
# 4. 값으로 정렬
course_summary = course_summary.sort_values(
    'completion_rate_pct', # 정렬 기준 컬럼
    ascending=False, # 내림차순 정렬
    ignore_index=True #인덱스 재구성
)
# pp(course_summary)

# 5.  월/과정 학습시간 피펏
study_pivot = merged.pivot_table(
    values= 'study_minutes', # 값 커럼
    index='month', # 행 컬럼
    columns='course', # 열 컬럼
    aggfunc=sum, # 집계함수
    fill_value=0, # 결측치 채우기
    margins=True, # 추가 한다
    margins_name='Total' # 토탈의 이름을 / 추가시 사용
)
# pp(study_pivot)

# 6. 월/카테로기 완료율 피펏
completion_pivot = merged.pivot_table(
    values= 'completed', # 값 커럼
    index='month', # 행 컬럼
    columns='category', # 열 컬럼
    aggfunc='mean', # 집계함수
    fill_value=0, # 결측치 채우기
)
completion_pivot = (completion_pivot * 100).round(1)
pp(completion_pivot)

# 7. 전체 학습시간 검증
raw_total = merged['study_minutes'].sum() # 원본 학습 분 합계
pivot_total = study_pivot.loc['Total','Total'] # 피버후 학습분합계
pp(f'일치여부: {raw_total == pivot_total}')
















































































