# day11_ex.py
# 주제: lod/iloc 조회, 결측치, 중복, 형변환, 전처리 전후 비교

import os # 폴더와 파일 경로 처리 모듈(폴더와 파일경로만 사용)
import pandas as pd

from python.print_util import pp

assets_dir ='./asseset' # CSC 파일을 저장할 경로명
os.makedirs(assets_dir,exist_ok=True) # 폴더가 없다면 생성

# 원본 csv 파일 경로 생성
raw_csv_path = os.path.join(assets_dir,'day11_customer_inquiry_raw.csv')

# 정제 CSV 파일경로
clean_csv_path = os.path.join(assets_dir,'day11_customer_inquiry_clean.csv')

# 원본 샘플 데이터 딕셔너리 (10 행 6열)
sample_data = {
    "문의ID": ["Q001", "Q002", "Q003", "Q004", "Q005", "Q006", "Q002", "Q007", "Q008", "Q009"],
    "지역": ["서울", "부산", "서울", "대전", None, "서울", "부산", "인천", "서울", "대구"],
    "문의유형": ["결제", "배송", "환불", "결제", "배송", "환불", "배송", "회원", "배송", "결제"],
    "처리시간": ["12", "8", "15", "unknown", "20", "10", "8", None, "18", "13"],
    "만족도": [5, 4, None, 3, 4, 5, 4, None, 2, 4],
    "담당자": ["김대리", "이주임", "박대리", None, "최과장", "김대리", "이주임", "정대리", None, "박대리"],
}

# 딕셔너리 > 데이터프래임
sample_df = pd.DataFrame(sample_data)
pp(sample_df)
pp(sample_df.shape) # (10,6)
sample_df.info()
pp(sample_df.describe())

# 데이터프레임 > csv 원본 파일
sample_df.to_csv(raw_csv_path,index=False,encoding='utf-8-sig')

# csv 파일 > 데이터프레임
df = pd.read_csv(raw_csv_path,encoding='utf-8-sig')

# 데이터 프레임 복제(원본 데이터 프레임 보존하기위해)
before_df = df.copy()

# 원본 데이터 출력
pp(df.columns.to_list()) # 컬럼명을 리스트로 출력
pp(df.dtypes) # 컬럼 데이터 타입 출력

# loc : 레이블 / 조건 기반 조회
loc_sample = df.loc[0:2,['문의ID','지역','만족도']] # 0~2god, 3개 컬럼
pp(loc_sample) # 데이터 프레임
pp(type(loc_sample))  #<class 'pandas.DataFrame'>

# df['지역'] =='서울' : 조회할 행의 조건, 지역이 서울인 행들
seoul_rows = df.loc[df['지역']=='서울',['지역','문의ID','문의유형','처리시간']]
pp(seoul_rows)
# 인덱스 재구성 (0~~~) , drop=True : 기존 인덱스 제거
seoul_rows_reindex = seoul_rows.reset_index(drop=True)
pp(seoul_rows_reindex)

# iloc : 숫자(인덱스)위치 기반 조회
iloc_sample = df.iloc[0:3,0:3] # 0~2행, 0~2열
pp(iloc_sample)

# 결측치 (missing value)

pp(df.isna()) #불리언의 데이터 로 구성된 데이터프레임 T or F , 1 or 0

missing_by_column = df.isna().sum() # 각 컬럼의 결측치 수
pp(missing_by_column) # Series
pp(type(missing_by_column))  #<class 'pandas.Series'>

pp(df.isna().sum().sum()) # 전체 결측치 수, 시리즈의 합계

# 하나 이상의 결측치가 있는 행들
rows_with_missing = df.loc[df.isna().any(axis=1)]
pp(rows_with_missing)

# 중복 데이터

duplicated_flags = df.duplicated()
pp(duplicated_flags)  # 중복여부의 불타입 Series

pp(df.duplicated().sum()) # 전체 중복 행의 수

duplicated_rows = df.loc[df.duplicated()]
pp(duplicated_rows)  # 중복된 6행이 나옴
pp(type(duplicated_rows))  # <class 'pandas.DataFrame'>

# 처리시간 컬럼을 숫자형으로 변환, 변환 불가하면 NaN으로 변환
df['처리시간'] = pd.to_numeric(df['처리시간'], errors='coerce')
pp(df['처리시간'])

# 숫자 변환 후 결측치 개수
pp(df['처리시간'].isna().sum())  # 2개

# 결측치 처리

# 처리시간 결측치를 중앙값으로 대체
processing_time_median = df['처리시간'].median()
df['처리시간'] = df['처리시간'].fillna(processing_time_median)
pp(df['처리시간'])

# 만족도 결측치 중앙값으로 대체
satisfaction_time_median = df['만족도'].median()
df['만족도'] = df['만족도'].fillna(satisfaction_time_median)
pp(df['만족도'])

# 지역 컬럼 최빈값 계산
region_mode = df['지역'].mode()[0]

# 지역 결측치를 최빈값으로 대체
df['지역'] = df['지역'].fillna(region_mode)
pp(df['지역'])

# 담당자 컬럼 고정 문자열로 대체
df['담당자'] = df['담당자'].fillna('미배정')
pp(df['담당자'])

# 결측치 처리 후 결측치 합계
pp(df.isna().sum())

# 중복 데이터 제거
df = df.drop_duplicates()

# 중복 데이터 제거 후 인덱스 0 부터 정리
df = df.reset_index(drop=True)

# 중복 데이터 제거후 행의 수
pp(df.shape[0]) # 9게, 1개의 중복 데이터 삭제됨

# 데이터 타입 변환
df['처리시간'] = df['처리시간'].astype('int64')
df['만족도'] = df['만족도'].astype('int64')
pp(df.dtypes)

# 전처리 결과 조건 조회

good_service = df.loc[
    (df['만족도']>=4) & (df['처리시간']<=15), # 행조건
    ['문의ID','지역','문의유형','처리시간','만족도']
]
pp(good_service)

# 전처리 전후 비교

rows_before = before_df.shape[0] # 전처리 이전의 행의 수
rows_after = df.shape[0] # 전처리 이후의 행의 수

missing_total_before = before_df.isna().sum().sum()
duplicate_count_before = before_df.duplicated().sum()

missing_total_after = df.isna().sum().sum() # 전처리 이후 결측치 수
duplicate_count_after = df.duplicated().sum() # 전처리 이후 중복 행 수


comparison_df = pd.DataFrame({
    '점검항목' : ['행 수','전체 결측치 수','중복 행 수'],
    '전처리전' : [rows_before,missing_total_before,duplicate_count_before],
    '전처리후' : [rows_after,missing_total_after,duplicate_count_after],
})
pp(comparison_df)

# 전치리한 데이터의 기초 통계
pp(df[['처리시간','만족도']].describe())

# 전처리한 데이터 프레임 > CSV 파일로 저장
df.to_csv(clean_csv_path,index=False,encoding='utf-8-sig')
pp('천처리 데이터 CSV 저장 완료!')


