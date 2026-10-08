# day12_extra.py

import pandas as pd
from python.print_util import pp

# 1. 데이터 불러오기
titles = pd.read_csv("./assets/titles_ko.csv")
credits = pd.read_csv("./assets/credits_ko.csv")
# pp(titles.shape) #(6137, 15)
# pp(credits.shape) (81355, 5)
# pp(titles.columns.to_list())
# #['콘텐츠ID', '제목', '유형', '설명', '공개연도', '연령등급', '상영시간', '장르', '제작국가', '시즌수', 'IMDb_ID', 'IMDb_평점', 'IMDb_투표수', 'TMDb_인기도', 'TMDb_평점']
# pp(credits.columns.to_list())
# #['인물ID', '콘텐츠ID', '이름', '배역', '역할']

# 2. 직픔 유형별 작품수
type_count = (
    titles.groupby("유형")
    .size()#행의수
    .sort_values(ascending=False) # 값에 대해서 내림차순 정렬
)
# pp(type_count)
# #유형
# MOVIE    3831
# SHOW     2306
# dtype: int64

# 3.작품 유형별 주요 통계
type_state = (
    titles.groupby('유형')
    .agg(
        작품수 = ('콘텐츠ID','count'),
        평균사영시간 = ('상영시간','mean'),
        평균IMDb평점 = ('IMDb_평점','mean'),
        최고IMDb평점 = ('IMDb_평점','max'),
    )
)
# 수정: type_count → type_state
# pp(type_state.round(2))

# 4. 공개 연도별 작품수 TOP 10
year_top10 = (
    titles.groupby('공개연도')
    .size() # 공개연도 각각의 행의 수
    .sort_values(ascending=False)
    .head(10)
)
# pp(year_top10)

# 5. 연령 등급별 작품 분석
age_stats = (
    titles.dropna(subset='연령등급') # 연령 등급 결측치 제거
    .groupby('연령등급')
    .agg(
        작품수=('콘텐츠ID', 'count'),
        평균IMDb평점=('IMDb_평점', 'mean'),
    ).sort_values('작품수',ascending=False).head(10)
)
# pp(age_stats.round(2))

# 6. 역할별 인원 및 참여 건수
role_stats = (
    credits.groupby('역할')
    .agg(
        참여건수=('콘텐츠ID', 'count'),
        고유인물수=('인물ID', 'nunique'),
    )
    .sort_values('참여건수',ascending=False)
)
# pp(role_stats)

# 7. 가장 많은 작품에 참여한 배우
actors = credits[credits['역할'] == 'ACTOR']

actor_top10 = (
    actors.groupby('이름')
    .agg(
        출연작품수=('콘텐츠ID', 'nunique'),
    )
    .sort_values('출연작품수', ascending=False)
    .head(10)
    .reset_index()
)
# pp(actor_top10)


# 8. 가장 많은 작품을 연출한 감독 TOP10
directors = credits[credits['역할'] == 'DIRECTOR']

director_top10 = (
    directors.groupby('이름')
    .agg(
        연출작품수=('콘텐츠ID', 'nunique'),
    )
    .sort_values('연출작품수', ascending=False)
    .head(10)
    .reset_index()
)
# pp(director_top10)


# 9. 작품별 배우수, 감독 수 계산
content_role_count = (
    credits.groupby(['콘텐츠ID', '역할'])
    .size()
    .unstack(fill_value=0)
)

# 10 특정 역할 컬럼이 없는 경우 보정
if 'ACTOR' not in content_role_count.columns:
    content_role_count['ACTOR'] = 0

if 'DIRECTOR' not in content_role_count.columns:
    content_role_count['DIRECTOR'] = 0

content_role_top10 = (
    content_role_count
    .sort_values('ACTOR', ascending=False)
    .head(10)
    .reset_index()
)

# pp(content_role_top10[['콘텐츠ID', 'ACTOR', 'DIRECTOR']])

# 11. 작품정보, 크래딧 정보 결합
merged = credits.merge(
    titles,
    on='콘텐츠ID',
    how='left',
    validate='many_to_one',
    indicator=True,
)
# pp(merged.shape) # (81355, 20)
# pp('_merged 값의 개수',merged['_merge'].value_counts())
# 양쪽에 있지 않는 것의 합계
not_matched_count = (merged['_merge'] != 'both').sum()
# pp(not_matched_count) # 0
# pp(not_matched_count==0) # True

# 12. 작품 유형별 배우/감독 참여 건수
type_role_count = (
    merged.groupby(['유형','역할'])
    .size()
    .reset_index(name='참여건수') # 인덱스명 부여해서 인덱스 재구성
    .sort_values('참여건수',ascending=False)
)
# pp(type_role_count)

#13. 평균 IMDb 평점이 높은 배우
actor_imdb = merged[
    (merged['역할']=="ACTOR") & # 배우 이면서
    (merged['IMDb_평점'].notna()) # 평점이 있음
]
actor_imdb_stats = (
    actor_imdb.groupby('이름')
    .agg(
        출연작품수=('콘텐츠ID','nunique'),
        평균IMDb평점 = ('IMDb_평점','mean'),
    )
)
actor_imdb_top10 = (
    actor_imdb_stats[actor_imdb_stats['출연작품수']>=10]
    .sort_values(
        ['평균IMDb평점','출연작품수'],
        ascending=[False,False],
    )
)
actor_imdb_top10['평균IMDb평점'] = (
    actor_imdb_top10['평균IMDb평점'].round(2)
)
# pp(actor_imdb_top10)

# 14. 평균 IMDb 평점이 높은 감독
director_imdb = merged[
    (merged['역할'] == 'DIRECTOR') &
    (merged['IMDb_평점'].notna())
]

director_imdb_stats = (
    director_imdb
    .groupby('이름')
    .agg(
        연출작품수=('콘텐츠ID', 'nunique'),
        평균IMDb평점=('IMDb_평점', 'mean')
    )
)

director_imdb_top10 = (
    director_imdb_stats[director_imdb_stats['연출작품수'] >= 5]
    .sort_values(
        ['평균IMDb평점', '연출작품수'],
        ascending=[False, False]
    )
    .head(10)
    .reset_index()
)

director_imdb_top10['평균IMDb평점'] = (
    director_imdb_top10['평균IMDb평점'].round(2)
)

# pp(director_imdb_top10)

# 15. concat을 이용한 DataFram 결합
actors = credits[credits['역할']=="ACTOR"].copy()
directors = credits[credits['역할']=="DIRECTOR"].copy()

credits_concat = pd.concat(
    [actors, directors], # 결합할 2개의 데이터 프레임
    ignore_index=True, #인덱스 잭성
)
# pp('actor 행수: ',len(actors)) #actor 행수:  76570
# pp('directors 행수: ',len(directors)) #directors 행수:  4785
# pp('credits_concat 행수: ',len(credits_concat)) #credits_concat 행수:  81355
# pp('credits 행수: ',len(credits)) # credits 행수:  81355

# 결합 결과 행 수 확인
# pp(len(actors)+ len(directors)==len(credits_concat)) # True 둘다 같다

# 원본과 같은지 확인
# pp(len(credits_concat) == len(credits)) # True

# 16. 종합 분석 : 평점이 높고 출연진이 많은 작품 찾기

# 콘텐츠ID 와 역할별 참여 인원 수 계산
staff_count = (
    credits.groupby(['콘텐츠ID','역할'])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)
# 컬럼이 없는 경우를 대비
if 'ACTOR' not in staff_count.columns:
    staff_count['ACTOR'] = 0

if 'DIRECTOR' not in staff_count.columns:
    staff_count['DIRECTOR'] = 0

# 한글 컬럼명으로 변경
staff_count = staff_count.rename(
    columns={
        'ACTOR': '배우수',
        'DIRECTOR': '감독수'
})

# 17. 작품 정보와 결합
title_staff = titles.merge(
    staff_count,
    on = '콘텐츠ID',
    how='left',
    validate='one_to_one',
)

# credits 에 없는 작품은 배우수/감독수가 결측치가 되므로 0으로 처리
title_staff[['배우수','감독수']]=(
    title_staff[['배우수','감독수']]
    .fillna(0)
    .astype(int)
)

# 조건 필터링
best_titles = title_staff[
    (title_staff['IMDb_평점'].notna())&
    (title_staff['IMDb_평점']>= 8.0) &
    (title_staff['배우수'] >= 10)
]

# IMDb 투표수가 많은 순서대로 정렬
best_titles = (
    best_titles.sort_values(
        ['IMDb_투표수','IMDb_평점'],
        ascending=[False,False],
    )[['제목','유형','공개연도','IMDb_평점','IMDb_투표수','배우수','감독수']]
    .head(20)
)
# 문자열 타입으로 변환후 출력, 인덱스로 사용하지 않음
pp(best_titles.to_string(index=False))





