# day11_extra.py
import pandas as pd

from python.print_util import pp

# CSV → DataFrame변환 원본
kd_df = pd.read_csv('kdrama_ko.csv',encoding='utf-8-sig')
pp(kd_df)

s_kd_df = kd_df.copy() # 복제본

#복제본 타입 변환
s_kd_df['평점'] = s_kd_df['평점'].astype('float64')
s_kd_df['방영연도'] = s_kd_df['방영연도'].astype('int64')
s_kd_df['회차'] = s_kd_df['회차'].astype('int64')

#이 상치 판정
# - 평점: 0점 이상 10점 이하
# - 방영연도: 2000년 이상 2030년 이하
# - 회차: 1회 이상 200회 이하
outlier_detection_data = s_kd_df.loc[
    (s_kd_df['평점'] >= 0.0) & (s_kd_df['평점'] <= 10.0) &
    (s_kd_df['방영연도'] >= 2000) & (s_kd_df['방영연도'] <= 2030) &
    (s_kd_df['회차'] >= 1) & (s_kd_df['회차'] <= 200)
]
pp(outlier_detection_data)

# [문제 1] CSV 파일을 DataFrame으로 변환하기.
# - DataFrame의 앞 5행을 출력하십시오.
pp(kd_df.head())


# [문제 2] 데이터의 전체 구조 확인하기
# 다음 내용을 각각 출력하십시오.

# - 전체 행 수와 열 수
pp(s_kd_df.shape) # (257,17)

# - 전체 컬럼명
pp(s_kd_df.columns.to_list()) # 컬럼명을 리스트로 출력
# - 컬럼별 dtype
pp(s_kd_df.dtypes)
# - `info()` 결과]
s_kd_df.info()
#
# [문제 3] 결측치 확인하기 다음 내용을 출력하십시오.
# - 각 컬럼별 결측치 개수
count_columns = s_kd_df.isna().sum()
pp(count_columns) # 각 컬럼 결측치
# - DataFrame 전체의 결측치 개수
all_count_columns = s_kd_df.isna().sum().sum()
pp(all_count_columns)  # 49개

# [문제 4] 결측치가 존재하는 컬럼만 확인하기 컬럼별 결측치 개수를
# 계산한 뒤 결측치가 1개 이상 존재하는 컬럼만 출력하십시오.
over_one = s_kd_df.isna().sum()
over_one = over_one[
    over_one >= 1
]
pp(over_one)

# [문제 5] 결측치가 포함된 행 조회하기 하나 이상의 결측치가 포함된 행만 추출하여 출력하십시오.
# `loc`를 이용하여 결측치가 포함된 행을 조회하십시오.
missing_row = s_kd_df.loc[
    s_kd_df.isna().any(axis=1)
]
pp(missing_row)

# [문제 6] 결측치 처리 방법 비교하기 `평점` 컬럼을 대상으로 다음 두 방법을 비교하십시오.

# 1. 결측치가 있는 행을 삭제한 별도의 DataFrame 생성
s_kd_df_out = s_kd_df.copy()
# '평점' 컬럼에 결측치(NaN)가 있는 행을 제거합니다.
s_kd_df_out = s_kd_df_out.dropna(subset=['평점'])

# 2. 결측치를 평점의 중앙값으로 대체한 별도의 DataFrame 생성
s_kd_df_out_median = s_kd_df.copy()
# '평점' 컬럼의 중앙값(Median)을 구합니다.
rating_median = s_kd_df_out_median['평점'].median()
# '평점' 컬럼의 결측치를 위에서 구한 중앙값으로 채웁니다.
s_kd_df_out_median['평점'] = s_kd_df_out_median['평점'].fillna(rating_median)
'''
s_kd_df_out [결측치 행 삭제 결과]
s_kd_df_out_median [결측치 중앙값 대체 결과]
'''
# 결과 확인 (pp 대신 기본 print 또는 display 사용 가능)
print("[결측치 행 삭제 결과]")
print(s_kd_df_out) # [252 rows x 17 columns]
print("\n[결측치 중앙값 대체 결과]")
print(s_kd_df_out_median) # [257 rows x 17 columns]
# 두 DataFrame의 행 수를 비교하여 출력하십시오.
# 원본 `df`는 이 문제에서 직접 변경하지 마십시오.

# [문제 7] 중복행 확인하기 다음 내용을 출력하십시오.
# - 전체 중복행 개수
pp('전체 중복행 개수',s_kd_df_out.duplicated().sum()) # 7개
pp('전체 중복행 개수',s_kd_df_out_median.duplicated().sum()) #7개
# - 실제 중복된 행
real_dp_rows = s_kd_df_out[s_kd_df_out.duplicated()]
print("\n[실제 중복된 행 데이터]")
print(real_dp_rows)

# [문제 8] 중복행 제거하기
# 원본 `df`의 복사본을 `clean_df`로 만든 뒤 다음 작업을 수행하십시오.
# - 완전히 동일한 중복행을 제거하십시오.
clean_df = s_kd_df_out.copy()
clean_df = clean_df.drop_duplicates()
# - Index를 0부터 다시 정리하십시오.
clean_df = clean_df.reset_index(drop=True)
# - 제거 전후 행 수를 출력하십시오.
pp(clean_df)
# - 중복행이 완전히 제거되었는지 다시 확인하십시오.
# pp(clean_df.duplicated().sum()) # 0

# [문제 9] 평점 이상치 탐지하기
# 정상 평점 범위를 0점 이상 10점 이하라고 가정합니다.
# `loc`와 조건식을 이용하여 다음 조건에 해당하는 행을 출력하십시오.
# ```text
# 평점 < 0
# 또는
# 평점 > 10
# ```
# 출력 컬럼
#
# - 제목
# - 방영연도
# - 평점
rating_outlier = clean_df.loc[
    (clean_df['평점'] < 0) | (clean_df['평점'] > 10),
    ['제목', '방영연도', '평점']
]
pp(rating_outlier)


# [문제 10] 방영연도 이상치 탐지하기
# 정상적인 방영연도를 2000년 이상 2030년 이하라고 가정합니다.
# 정상 범위를 벗어나는 행만 조회하십시오.
# 출력 컬럼
# - 제목
# - 방영연도
year_outlier = clean_df.loc[
    (clean_df['방영연도'] < 2000) | (clean_df['방영연도'] > 2030),
    ['제목', '방영연도']
]
pp(year_outlier)

# [문제 11] 회차 이상치 탐지하기
# 정상 회차 범위를 1회 이상 200회 이하라고 가정합니다.
# 다음 조건의 데이터를 조회하십시오.
#
# ```text
# 회차 <= 0
# 또는
# 회차 > 200
# ```
# 출력 컬럼
# - 제목
# - 회차
count_outlier = clean_df.loc[
    (clean_df['회차'] <= 0) | (clean_df['회차'] > 200),
    ['제목', '회차']
]
pp(count_outlier)

# [문제 12] 이상치 처리하기
# `clean_df`를 대상으로 다음 작업을 수행하십시오.
# - 평점의 정상 범위를 벗어나는 값을 결측치로 변경하십시오.
# - 방영연도의 정상 범위를 벗어나는 값을 결측치로 변경하십시오.
# - 회차의 정상 범위를 벗어나는 값을 결측치로 변경하십시오.
# 이후 다음 기준으로 결측치를 대체하십시오.
clean_vudwja_avg = clean_df.loc[ (clean_df['평점'] >= 0) & (clean_df['평점'] <= 10), '평점' ].median()
clean_duseh_avg = clean_df.loc[ (clean_df['방영연도'] >= 2000) & (clean_df['방영연도'] <= 2030), '방영연도' ].median()
clean_ghlck_avg = clean_df.loc[ (clean_df['회차'] >= 1) & (clean_df['회차'] <= 200), '회차' ].median()

# - 평점 → 정상 데이터의 중앙값
# - 방영연도 → 정상 데이터의 중앙값
# - 회차 → 정상 데이터의 중앙값
clean_df.loc[
    (clean_df['평점'] < 0) | (clean_df['평점'] > 10),
    '평점'
] = clean_vudwja_avg

clean_df.loc[
    (clean_df['방영연도'] < 2000) | (clean_df['방영연도'] > 2030),
    '방영연도'
] = clean_duseh_avg

clean_df.loc[
    (clean_df['회차'] <= 0) | (clean_df['회차'] > 200),
    '회차'
] = clean_ghlck_avg
# 처리 후 세 컬럼에 이상치가 남아 있는지 다시 확인하십시오.

# [문제 13] 나머지 결측치 처리하기
# `clean_df`의 문자열 계열 컬럼에 남아 있는 결측치를 `"정보없음"`으로 대체하십시오.
# 다음 컬럼을 대상으로 처리합니다.
# - 방영일
# - 방송사
# - 방영요일
# - 시청등급
# - 장르
# - 태그
# - 감독
# - 극본
# - 출연진
# - 제작사
n_data = '정보없음'
clean_df['방영일'] = clean_df['방영일'].fillna(n_data)
clean_df['방송사'] = clean_df['방송사'].fillna(n_data)
clean_df['방영요일'] = clean_df['방영요일'].fillna(n_data)
clean_df['시청등급'] = clean_df['시청등급'].fillna(n_data)
clean_df['장르'] = clean_df['장르'].fillna(n_data)
clean_df['태그'] = clean_df['태그'].fillna(n_data)
clean_df['감독'] = clean_df['감독'].fillna(n_data)
clean_df['극본'] = clean_df['극본'].fillna(n_data)
clean_df['출연진'] = clean_df['출연진'].fillna(n_data)
clean_df['제작사'] = clean_df['제작사'].fillna(n_data)
# 처리 후 전체 결측치 개수를 출력하십시오.
pp(clean_df.isna().sum().sum()) # 0개

# [문제 14] 컬럼 자료형 변환하기
# 다음과 같이 자료형을 정리하십시오.
# - `방영연도` → 정수형
# - `회차` → 정수형
# - `평점` → 실수형
# - `순위` → `#` 문자를 제거한 뒤 정수형
# - `제목` → Pandas string 자료형
# 변환 후 `dtypes`를 출력하십시오.
clean_df['방영연도'] = clean_df['방영연도'].astype('int64')
clean_df['회차'] = clean_df['회차'].astype('int64')
clean_df['평점'] = clean_df['평점'].astype('float64')
clean_df['순위'] = clean_df['순위'].str.replace('#', '').astype('int64')
clean_df['제목'] = clean_df['제목'].astype('string')
pp(clean_df.dtypes)

# [문제 15] 전처리 전후 비교 및 저장하기
# 원본 DataFrame과 정제된 `clean_df`를 비교하여
# 다음 형태의 DataFrame을 생성하십시오.
# ```text
# 점검항목        전처리전        전처리후
# 행 수
# 전체 결측치
# 중복행 수
# 평점 이상치
# 방영연도 이상치
# 회차 이상치
# ```

# 전처리 전 이상치 개수
before_rating_outlier = (
    (kd_df['평점'] < 0) | (kd_df['평점'] > 10)
).sum()

before_year_outlier = (
    (kd_df['방영연도'] < 2000) | (kd_df['방영연도'] > 2030)
).sum()

before_count_outlier = (
    (kd_df['회차'] <= 0) | (kd_df['회차'] > 200)
).sum()


# 전처리 후 이상치 개수
after_rating_outlier = (
    (clean_df['평점'] < 0) | (clean_df['평점'] > 10)
).sum()

after_year_outlier = (
    (clean_df['방영연도'] < 2000) | (clean_df['방영연도'] > 2030)
).sum()

after_count_outlier = (
    (clean_df['회차'] <= 0) | (clean_df['회차'] > 200)
).sum()


# 전처리 전후 비교 DataFrame 생성
compare_df = pd.DataFrame({
    '점검항목': [
        '행 수','전체 결측치','중복행 수','평점 이상치','방영연도 이상치','회차 이상치'
    ],

    '전처리전': [
        kd_df.shape[0],kd_df.isna().sum().sum(),kd_df.duplicated().sum(),
        before_rating_outlier,before_year_outlier,before_count_outlier
    ],

    '전처리후': [
        clean_df.shape[0],clean_df.isna().sum().sum(),clean_df.duplicated().sum(),
        after_rating_outlier,after_year_outlier,after_count_outlier
    ]
})

pp(compare_df)


# 추가로 다음 작업을 수행하십시오.
# - 정제 후 평점이 높은 상위 10개 드라마를 출력하십시오.
# - 출력 컬럼은 `순위`, `제목`, `방영연도`, `평점`으로 하십시오.
# - 평점을 기준으로 내림차순 정렬하십시오.

top10_df = clean_df.sort_values(
    by='평점',
    ascending=False
).head(10).reset_index(drop=True)

top10_df = top10_df[
    ['순위', '제목', '방영연도', '평점']
]

pp(top10_df)


# - 최종 DataFrame을 `kdrama_clean.csv` 파일로 저장하십시오.
# - 저장 시 Index는 제외하고 `utf-8-sig` 인코딩을 사용하십시오.

clean_df.to_csv(
    'kdrama_clean.csv',
    index=False,
    encoding='utf-8-sig'
)


# [실습 마무리 확인]
# 전처리 후 다음 조건을 만족하는지 확인하십시오.
# - 중복행이 존재하지 않는가?
pp(clean_df.duplicated().sum())

# - 결측치가 모두 처리되었는가?
pp(clean_df.isna().sum().sum())

# - 평점이 0~10 범위에 있는가?
pp(((clean_df['평점'] < 0) | (clean_df['평점'] > 10)).sum())

# - 방영연도가 2000~2030 범위에 있는가?
pp(((clean_df['방영연도'] < 2000) | (clean_df['방영연도'] > 2030)).sum())

# - 회차가 1~200 범위에 있는가?
pp(((clean_df['회차'] <= 0) | (clean_df['회차'] > 200)).sum())

# - 순위가 숫자형으로 변환되었는가?
pp(clean_df['순위'].dtype)

# - 원본 파일과 정제 파일을 구분하여 보존했는가?
pp(kd_df.head())
pp(clean_df.head())


'''
# [결측치를 확인하는 이유]
# 결측치(NaN)가 있으면 계산이나 분석 결과가 정확하지 않을 수 있기 때문에
# 어떤 컬럼에 결측치가 있는지 먼저 확인한다.

# [결측치가 있는 행을 삭제하는 이유]
# 결측치가 있는 데이터를 분석에서 제외하기 위해 삭제한다.
# 단, 행을 삭제하기 때문에 전체 데이터의 개수가 줄어든다.

# [결측치를 중앙값으로 대체하는 이유]
# 데이터를 삭제하지 않고 기존 행을 유지하면서 결측치를 처리할 수 있다.
# 중앙값은 데이터의 가운데에 위치한 값이라 이상치의 영향을 비교적 적게 받는다.

# [이상치를 처리하는 이유]
# 정상 범위를 크게 벗어난 값은 분석 결과를 왜곡할 수 있기 때문에 처리한다.

# [이상치를 제외한 정상 데이터로 중앙값을 구하는 이유]
# 이상치가 대표값 계산에 영향을 주는 것을 막기 위해
# 정상 범위의 데이터만 사용해서 중앙값을 구한다.

# [중복행을 제거하는 이유]
# 같은 데이터가 여러 번 존재하면 특정 데이터가 중복으로 계산되어
# 분석 결과가 부정확해질 수 있기 때문에 제거한다.

# [reset_index(drop=True)를 사용하는 이유]
# 행을 삭제하면 기존 인덱스 번호가 중간중간 비게 될 수 있기 때문에
# 인덱스를 0부터 다시 순서대로 정리한다.
# drop=True는 기존 인덱스를 새로운 컬럼으로 남기지 않고 버린다는 뜻이다.

# [자료형을 변환하는 이유]
# 숫자는 계산할 수 있는 숫자형으로, 문자열은 문자열 자료형으로 맞춰야
# 각 데이터에 알맞은 연산과 분석을 할 수 있다.

# [전처리 전후를 비교하는 이유]
# 결측치, 중복행, 이상치 등이 실제로 제대로 처리되었는지 확인하기 위해 비교한다.

# [원본 DataFrame을 복사해서 사용하는 이유]
# 전처리 과정에서 데이터가 변경되더라도 원본 데이터를 보존하기 위해 복사본을 사용한다.

# [CSV 저장 시 index=False를 사용하는 이유]
# DataFrame의 인덱스 번호를 CSV의 새로운 컬럼으로 저장하지 않기 위해 사용한다.

# [utf-8-sig를 사용하는 이유]
# 한글이 포함된 CSV 파일을 Excel 등에서 열었을 때
# 한글이 깨지는 문제를 줄이기 위해 사용한다.
'''