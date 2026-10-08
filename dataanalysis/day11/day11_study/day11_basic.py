# day11_basic.py
# AI휴먼 11일차 Basic 과제
# 주제: 도서관 대출 데이터 정제
#
# 상황
# 도서관에서 대출 현황 CSV를 전달받았습니다.
# 일부 값이 비어 있고 동일한 대출 기록이 반복되어 있으며, 대출일수가 문자열로 저장되어 있습니다.
# 분석 전에 기본적인 데이터 정제를 수행하십시오.
#
#
# 사용 데이터
#
# 대출ID,도서분류,대출일수,연체일수,회원등급
# L001,IT,7,0,일반
# L002,경제,14,3,우수
# L003,문학,10,0,
# L004,IT,unknown,2,일반
# L005,과학,21,5,우수
# L002,경제,14,3,우수
# L006,문학,7,0,일반

import pandas as pd

from python.print_util import pp


sample_data = {
    '대출ID' :['L001','L002','L003','L004','L005','L002','L006'],
    '도서분류' : ['IT','경제','문학','iT','과학','경제','문학'],
    '대출일수' : ['7','14','10','unknown','21','14','7'],
    '연체일수' : ['0','3','0','2','8','3','0'],
    '회원등급' : ['일반','우수','','일반','우수','우수','일반']
}


pp(sample_data)
# 요구사항
#
# 아래 데이터를 day11_library_raw.csv로 생성한 뒤 Pandas로 읽으십시오.
sample_data = pd.DataFrame(sample_data) # 딕셔너리 > 데이터 프레임
# 데이터 프레임 > csv 파일
sample_data.to_csv('day11_library_raw.csv', index=False,encoding='utf-8-sig')
# 파일 읽기
df = pd.read_csv('day11_library_raw.csv',encoding='utf-8-sig')
# head(), shape, dtypes로 원본 구조를 확인하십시오.
pp(sample_data.head())
pp(sample_data.shape)
pp(sample_data.dtypes)

# 연체 일수를 숫자로 반한
df['연체일수'] = pd.to_numeric(df['연체일수'], errors='coerce')
pp(df['연체일수'])
# loc를 이용해 연체일수가 1일 이상인 행에서 대출ID, 도서분류, 연체일수만 출력하십시오.
pp(df.loc[df['연체일수'] >= 1,['대출ID', '도서분류', '연체일수']])

# iloc를 이용해 앞 4행과 앞 3열을 출력하십시오.
pp(df.iloc[0:4,0:3])

# 컬럼별 결측치 개수를 출력하십시오.
num_nothing = df.isna().sum()
pp(num_nothing)

# 전체 중복 행 수를 출력하십시오.
pp(df.duplicated()) # 중복 5
dul_coulmn = df.iloc[df.duplicated()] # 중복 컬럼 인덱스로 찾기
pp(dul_coulmn)

# 대출일수를 pd.to_numeric(errors="coerce")로 숫자형으로 변환하십시오.
df['대출일수'] = pd.to_numeric(df['대출일수'], errors='coerce')
pp(df['대출일수'])


# 대출일수의 결측치는 중앙값으로 대체하십시오.
rt_day_median = df['대출일수'].median()
df['대출일수'] = df['대출일수'].fillna(rt_day_median)
pp(df['대출일수'])

# 회원등급의 결측치는 "일반"으로 대체하십시오.
df['회원등급'] = df['회원등급'].fillna('일반')
pp(df['회원등급'])

# 중복 행을 제거하십시오.
df = df.drop_duplicates()
pp(df)
# 중복 제거후 인덱스 정리
df = df.reset_index(drop=True)
pp(df)
# 대출일수를 정수형으로 변환하십시오.
df['대출일수'] = df['대출일수'].astype('int64')
pp(df['대출일수'])
# 전처리 후 shape, 결측치 개수, 중복 행 수, dtypes를 출력하십시오.
pp(df.shape)
pp(df.isna().sum())
pp(df.duplicated().sum())
pp(df.dtypes)







