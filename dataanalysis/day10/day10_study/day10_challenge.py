# Day 10 Challenge 과제 - 채용 지원자 데이터 사전 만들기

import pandas as pd
from python.print_util import pp

# 지원자 데이터
applicant_data = [
    ['A001', '백엔드',     '컴퓨터공학', 1, 82, 845],
    ['A002', '데이터분석', '통계학',     0, 91, 910],
    ['A003', '프론트엔드', '디자인',     2, 78, 800],
    ['A004', 'AI엔지니어', '전자공학',   1, 94, 880],
    ['A005', '백엔드',     '경영학',     3, 75, 920],
    ['A006', '데이터분석', '수학',       1, 89, 870],
    ['A007', 'AI엔지니어', '컴퓨터공학', 2, 96, 935],
    ['A008', '프론트엔드', '컴퓨터공학', 0, 84, 825],
    ['A009', '백엔드',     '전자공학',   1, 87, 860],
    ['A010', '데이터분석', '경영학',     2, 81, 905]
]

# 2차원 리스트 → 데이터 프레임
source_df = pd.DataFrame(
    applicant_data,
    columns=['지원ID', '지원직무', '전공', '경력년수', '코딩테스트', '영어점수']
)

# 데이터 프레임 → csv 파일
source_df.to_csv(
    './applicants.csv',
    index=False,
    encoding='utf-8-sig'
)

# csv 파일 → 데이터 프레임
applicants_df = pd.read_csv(
    './applicants.csv',
    encoding='utf-8-sig'
)

# 처음 5개 행
print(applicants_df.head())
pp(applicants_df.head())

#마지막 5개행
pp(source_df.tail())

pp(applicants_df.shape) #(10,6) 행과 열의 수

pp(list(source_df.columns)) # 컬럼명들

pp(applicants_df.dtypes) #dtype: object
pp(type(applicants_df.dtypes)) #<class 'pandas.Series'>
print('[info]\n')
applicants_df.info() #<class 'pandas.DataFrame'>

# 2개의 컬럼만 추출한 데이터 프레임
score_df = applicants_df[['코딩테스트','영어점수']]
pp(score_df)
pp(score_df.describe()) # 기초통계

pp(applicants_df['지원직무'].value_counts()) # 직무별 지원자수
pp(type(applicants_df['지원직무'].value_counts())) #<class 'pandas.Series'>

pp(applicants_df['전공'].unique()) # 고유 전공 문자열 배열
pp(type(applicants_df['전공'].unique())) # <class 'pandas.arrays.StringArray'>

pp(applicants_df['전공'].nunique()) # 고유 전공수

dictionary_rows = [] #데이터 사전의 각행 저장할 리스트

for column in applicants_df.columns: # 컬럼 수만큼 반복
    series = applicants_df[column] # 컬럼 > 시리즈 로 바꿈
    dictionary_rows.append({ # 리스트에 딕셔너리(행) 추가
        '컬럼명' : column,
        'dtype' : str(series.dtype),
        '전체행수' : len(series),
        'Non-Null' : series.count(),
        '고유값수' : series.nunique(),
        '첫번째예시값' : series.iloc[0] # 시리즈에서 0 번 인덱스 값
    })

# 리스트 > 딕셔너리 변환
data_dictionary = pd.DataFrame(dictionary_rows)
pp(data_dictionary)

# 데이터 사전 > csv 파일 변환
data_dictionary.to_csv(
    './applicants_data_dictionary.csv',
    index=False,
    encoding='utf-8-sig'
)

applicant_count= applicants_df.shape[0] # 전체 지원자 수 = 행의 수
column_count= applicants_df.shape[1]  # 열의수
job_type_count = applicants_df['지원직무'].unique()  # 직원 직무 종류 수
coding_average = applicants_df['코딩테스트'].mean() # 코딩 테스트 평슌

pp('전체 지원자 수',applicant_count)
pp('전체 컬럼수',column_count)
pp('전체 지원 직무 종류 수',job_type_count)
pp('코딩테스트 평균',coding_average)

pp('현재 단계에서는 데이터 구조와 통계만 확인 했으며, 정제 작업은 수행 하지 않음')

# print_util.py 코드
# def pp(*obj): # 출력 할떄마다 구분선
#     print(*obj)
#     print('-'*50)

