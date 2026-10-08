# day13_ex.py
# 주제: 문자열 처리, 날짜 타입, 범주형, 구간화, IQR
import pandas as pd
from python.print_util import pp

# 채용 데이터
df = pd.DataFrame({
    # 문자열 데이터
    "지원자": [" 김민수 ", "이서연", " 박준호", "최유진 ", "정하늘", "윤지호", "한소민", "오지훈"],
    # 범주형데이터
    "직무": [" Data Analyst ", "DATA ANALYST", "data  analyst", "AI Engineer", "ai engineer ", "Backend", "BACKEND ", "backend"],
    # 날짜 타입
    "지원일": ["2026-08-01", "2026/08/03", "2026-08-05", "2026-08-08", "invalid", "2026-08-15", "2026/08/17", "2026-08-20"],
    # 범주형
    "전형": ["서류", "면접", "서류", "과제", "면접", "서류", "과제", "면접"],
    # 숫자형
    "평가점수": [78, 84, 82, 91, 88, 76, 80, 190]
})

# df.info()

# 1. 문자열 공백 처리, 표기 정리
df['지원자'] = df['지원자'].str.strip() # 이름 앞뒤 공백 문자 제거
df['직무'] = (
    df['직무']
    .str.strip()
    .str.lower() # 소문자
    .str.replace(r'\s+',' ',regex=True) # 공백문자 1개 이상 연속되면 1개
)
# pp(df[['지원자','직무']])

# 2. 문자열 검색, 부분 추출

# 직무 컬럼의 문자열이 data 라는 문자열을 포함하면 True 아니면 False
df['데이터직무'] = df['직무'].str.contains('data', na=False)
# pp(df['데이터직무'])

# 직무 컬럼의 문자열에서 영문소문자가 1개 이상 반복되는 문자열로 시작하는
# 문자열을 추출
# expand=False : Series로 반환
df['직무첫단어'] = df['직무'].str.extract(
    r'^([a-z]+)',
    expand=False
)
# pp(df['직무첫단어'])

# 3. 날짜 문자열 > datetime
df['지원일'] = pd.to_datetime( # 날짜 타입으로 변환
    df['지원일'],
    errors='coerce', # 변환 불가시에는 NaT
    format='mixed', # 포맷 = 형식
)

# pp(df['지원일'].dtypes)
# pp(type(df['지원일'].dtypes))
# pp(df['지원일'].isna().sum()) # 1, NaT 1개

# 날짜 파생 변수 생성
df['지원연도'] = df['지원일'].dt.year
df['지원월'] = df['지원일'].dt.month
df['지원요일번호'] = df['지원일'].dt.dayofweek # 0 : 월
df['지원요일'] = df['지원일'].dt.day_name()
df['지원연월'] = df['지원일'].dt.strftime('%Y-%m')

# pp([
#     df['지원연도'],
#     df['지원월'],
#     df['지원요일번호'],
#     df['지원요일'],
#     df['지원연월']
# ])

# 기준일과 날짜 차이 계산
reference_date = pd.Timestamp('2026-08-31')

df['기준일까지경과일'] = (
    reference_date - df['지원일']
).dt.days

pp(df[['지원일', '기준일까지경과일']])

# 범주형 자료형 변환
df['전형'] = df['전형'].astype('category')

pp(df['전형'].cat.categories)
pp(df['전형'].cat.categories.tolist())


# 4. 순서형 범주 만들기
process_order = ['서류','면접','과제'] # 범주로 사용할 리스트
process_type = pd.CategoricalDtype( # 순서형 범주 타입
    categories=process_order, #범주리스트
    ordered=True # 순서있음
)
# 범주로 정렬하기 위해 전형을 순서형 범주 타입으로 변환
df['전형'] = df['전형'].astype(process_type)
pp(df.sort_values('전형')[['지원자','전형']]) # 전형 오름 차순 정렬 후 지원자, 전형 출력

# 점수를 고정 구간 범주로 변환
df['평가등급'] = pd.cut(
df['평가점수'], # 범주 기준 데이터
    # 구간 설정, float('inf') : 무한
    bins=[0,70,80,90,100,float('inf')],
    labels=['D','C','B','A','범위초과'], # 구간명
    include_lowest=True, # 최솟값을 구간에 포함
)
pp(df[['평가점수','평가등급']])

# 5. IQR 기준 계산
q1 = df['평가점수'].quantile(0.25) # 1사 분의 수, 1/4
q2 = df['평가점수'].quantile(0.5) # 2사 분의 수, 2/4
q3 = df['평가점수'].quantile(0.75) # 3사 분의 수, 3/4
iqr = q3 - q1  # 중간에 위치한 50% 범위
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr # 하한, 상한
pp(f'Q1={q1:.2f}, Q3={q3:.2f}, IQR={iqr:2f}')
pp(f'하한 ={lower:.2f}, 상한 = {upper:.2f}')

# 이상치 후보 탑지
# 평가 점수가 하한~상한이 아닌 점수의 사이인지 여부에 대한 불리언 시리즈
# between(A, B) : A와B를 포함한 사이의 범위
outlier_mask = ~df['평가점수'].between(lower, upper)
df['이상치여부']=outlier_mask
pp(outlier_mask)

# 원본 유지하면서 경계값으로 보정
df['평가점수_보정'] = df['평가점수'].clip(lower=lower,upper=upper)
pp(df[['평가점수','평가점수_보정']]) # 190 > 102.625(상한으로 보정)

# 전처리 결과 검증
pp('날짜 NaT 수: ', df['지원일'].isna().sum())
pp('직무 고유값: ', sorted(df['직무'].unique()))
pp('전형 범주: ', list(df['전형'].cat.categories))
pp('이상치 후보 수: ', int(df['이상치여부'].sum()))














