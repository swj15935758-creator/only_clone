# # day11_application.py
# #AI휴먼 11일차 Application 과제
# 주제: 사내 교육 평가 데이터 전처리0

# 상황
# 인사팀에서 사내 교육 평가 데이터를 전달했습니다.
# 평가점수 컬럼에 문자열이 섞여 있고, 부서와 강사 정보에 결측치가 있으며,
# 동일한 교육 참여 기록도 포함되어 있습니다.
import pandas as pd

from python.print_util import pp

sample_data = {
    '사번': ['E101', 'E102', 'E103', 'E104', 'E105', 'E102', 'E106', 'E107'],
    '부서': ['개발', '기획', '', '마케팅', '개발', '기획', '개발', '마케팅'],
    '과정': ['Python', '데이터분석', 'Python', '데이터분석', 'AI', '데이터분석', 'AI', 'Python'],
    '평가점수': ['88', '92', '76', '미응시', '95', '92', '84', ''],
    '강사': ['김강사', '이강사', '김강사', '이강사', '', '이강사', '박강사', '김강사']
}
# 요구사항
#
# 아래 데이터를 day11_training_raw.csv로 생성한 뒤 Pandas로 읽으십시오.
tranning_raw_data = pd.DataFrame(sample_data) # 딕셔너리 > 데이터 프레임
tranning_raw_data.to_csv('day11_training_raw.csv',index=False,encoding='utf-8-sig') # 데이터 프레임 > csv 파일
df = pd.read_csv('day11_training_raw.csv',encoding='utf-8-sig') # 파일 읽기

# 원본의 행 수, 컬럼별 결측치 수, 중복 행 수, dtype을 기록하십시오.
pp('원본 행수',df.shape[0]) #원본 행수
column_non = df.isna().sum() # 컬럼별 결측치 수
pp('컬럼별 결측치 수\n',column_non)
dul_coulmn = df.duplicated().sum() # 중복 행수
pp('중복 행 수:',dul_coulmn)
pp('데이터 타입',df.dtypes)

# loc를 이용해 과정이 "데이터분석"인 행에서 사번, 부서, 평가점수를 출력하십시오.
data_analyist = df.loc[df['과정']=='데이터분석',['사번','부서','평가점수']]
pp('데분: \n',data_analyist)

# iloc를 이용해 마지막 3행과 사번, 부서, 과정에 해당하는 앞 3열을 출력하십시오.
pp(df.iloc[-3:,0:3])

# 평가점수를 pd.to_numeric(errors="coerce")로 변환하십시오.
# 원본을 남기기위해 샘플 만듬
sample_df = pd.read_csv('day11_training_raw.csv',encoding='utf-8-sig') # 파일 읽기
pp('변환전 개수',sample_df['평가점수'].isna().sum())
sample_df['평가점수'] = pd.to_numeric(sample_df['평가점수'], errors='coerce')

pp(sample_df['평가점수'].dtype) # 샘플데이터
# 변환 후 평가점수에 새로 발생한 결측치 개수를 출력하십시오.
pp('변환후 개수',sample_df['평가점수'].isna().sum())

# 평가점수 결측치는 중앙값으로 대체하십시오.
avg_vudrk = sample_df['평가점수'].median()#중앙값
# pp(avg_vudrk)
sample_df['평가점수'] = sample_df['평가점수'].fillna(avg_vudrk) #결측치 대체
pp(sample_df['평가점수'])

# 부서 결측치는 최빈값으로 대체하십시오.
pp(sample_df['부서'])
min_qntj = sample_df['부서'].mode()[0]
sample_df['부서'] = sample_df['부서'].fillna(min_qntj) #결측치 대체
pp(sample_df['부서'])

# 강사 결측치는 "미배정"으로 대체하십시오.
sample_df['강사'] = sample_df['강사'].fillna('미배정') #결측치 대체
pp(sample_df['강사'])

# 중복 행을 제거하고 Index를 다시 정리하십시오.
sample_df = sample_df.drop_duplicates()
sample_df = sample_df.reset_index(drop=True)
print(sample_df)


# 평가점수를 정수형으로 변환하십시오.
sample_df['평가점수'] = sample_df['평가점수'].astype('int64')
pp(sample_df['평가점수'].dtype)

# 평가점수가 85점 이상인 참여 기록만 loc로 조회하십시오.
excellent_score = sample_df.loc[
    (sample_df['평가점수'] >= 85)
]
pp(excellent_score)

# 전처리 전후를 비교하는 DataFrame을 다음 항목으로 만드십시오.
# 점검항목 / 전처리전 / 전처리후
# 행 수
before_df = df.shape[0]
aftter_df = sample_df.shape[0]
# 전체 결측치
before_non = df.isna().sum().sum()
after_non = sample_df.isna().sum().sum()
# 중복 행
before_dul = df.duplicated().sum()
after_dul = sample_df.duplicated().sum()

comparison_df = pd.DataFrame({
    '점검항목': ['행 수', '전체 결측치 수', '중복 행 수'],
    '전처리전': [before_df,before_non,before_dul],
    '전처리후': [aftter_df,after_non,after_dul]
})
pp(comparison_df)
# 정제 데이터를 day11_training_clean.csv로 저장하십시오.

comparison_df.to_csv('day11_training_clean.csv',index=False,encoding='utf-8-sig')

# 사용 데이터

# 사번,부서,과정,평가점수,강사
# E101,개발,Python,88,김강사
# E102,기획,데이터분석,92,이강사
# E103,,Python,76,김강사
# E104,마케팅,데이터분석,미응시,이강사
# E105,개발,AI,95,
# E102,기획,데이터분석,92,이강사
# E106,개발,AI,84,박강사
# E107,마케팅,Python,,김강사
