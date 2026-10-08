# day13_application.py
# 주제:AI휴먼 13일차 Application 과제
# 주제: 온라인 강의 이용로그 정제 및 분석용 컬럼 생성
#
# 아래 데이터를 사용하십시오.
#
import pandas as pd

from python.print_util import pp

df = pd.DataFrame({
    "학습자ID": [" S001 ", "S002", " s003", "S004 ", "S005", "s006", "S007", "S008"],
    "강의명": [" Python Data ", "PYTHON DATA", "python  data", "LLM Basic", "llm basic ", "Prompt", "PROMPT ", "prompt"],
    "접속일": ["2026-08-01", "2026/08/02", "2026-08-03", "2026-08-04", "error", "2026/08/06", "2026-08-07", "2026-08-08"],
    "접속기기": ["PC", "mobile", "Mobile", "pc", "TABLET", "tablet", "PC", "mobile"],
    "시청분": [42, 58, 35, 70, 63, 51, 47, 720],
    "진도율": [35, 48, 62, 77, 85, 91, 100, 56]
})

# 요구사항
# 학습자ID의 공백을 제거하고 영문자를 대문자로 통일하십시오.
df['학습자ID'] = df['학습자ID'].str.strip().str.upper()
# 강의명은 소문자로 변환하고 연속 공백을 한 칸으로 정리하십시오.
df['강의명'] = (df['강의명']
             .str.strip().str.lower()
             .str.replace(r'\s+',' ',regex=True))
# 접속기기는 pc, mobile, tablet 세 범주로 표기를 통일하십시오.
connect_device =['pc','mobile','tablet']
connect_device_type = pd.CategoricalDtype(
    categories=connect_device,
    ordered=True
)
# 접속일을 datetime으로 변환하고 접속월, 접속요일, 접속연월 컬럼을 만드십시오.
df['접속일'] = pd.to_datetime(
    df['접속일'],
    errors='coerce',
    format = 'mixed',
)
df['접속월'] = df['접속일'].dt.month
df['접속요일'] = df['접속일'].dt.day_name()
df['접속연월'] = df['접속일'].dt.strftime('%Y-%m')
# pp(df)

# 접속기기를 category 자료형으로 변환하십시오.
df['접속기기'] = df['접속기기'].str.lower()
df['접속기기'] = df['접속기기'].astype('category')

# 진도율을 pd.cut()으로 다음 네 범주로 만드십시오.
# 0~49: 시작
# 50~74: 진행
# 75~99: 마무리
# 100: 완료
# 진도단계를 시작 < 진행 < 마무리 < 완료 순서의 순서형 범주로 만드십시오.
# 진도율를 고정 구간 범주로 변환

df['진도단계'] = pd.cut(
df['진도율'], # 범주 기준 데이터
    # 구간 설정, float('inf') : 무한
    bins=[0,49,74,99,100,float('inf')],
    labels=['시작','진행','마무리','완료','측정불가'], # 구간명
    include_lowest=True, # 최솟값을 구간에 포함
)
pp(df['진도단계'])


# 시청분에 대해 IQR 이상치 후보를 탐지하십시오.
# 이상치 원본은 삭제하지 말고 시청분_보정 컬럼을 만들어 IQR 하한/상한으로 clip() 하십시오.
q1 = df['시청분'].quantile(0.25) # 1사 분의 수, 1/4
q3 = df['시청분'].quantile(0.75) # 3사 분의 수, 3/4
iqr = q3 - q1  # 중간에 위치한 50% 범위
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr # 하한, 상한

df['시청분_보정'] = df['시청분'].clip(lower=lower,upper=upper)
pp(df['시청분_보정'])


# 전처리 후 아래 내용을 출력하십시오.
# 날짜 변환 실패 건수
pp('날짜 NaT 수: ', df['접속일'].isna().sum())
# 강의명 고유값
pp('강의명 고유값: ', sorted(df['강의명'].unique()))
# 접속기기 범주
pp('접속기기 범주: ', list(df['접속기기'].cat.categories))
# 진도단계별 건수
cut_result = pd.cut(
    df['진도율'],
    bins=[0,49,75,99,100,float('inf')],
    labels=['시작','진행','마무리','완료','측정불가'], # 구간명
    include_lowest=True,
)
# 진도단계를 순서형 범주로 변환
progress_type = pd.CategoricalDtype(
    categories=['시작', '진행', '마무리', '완료'],
    ordered=True
)
pp(cut_result.value_counts(sort=False))

# 이상치 후보 수
outlier_mask = ~df['시청분'].between(lower, upper)
df['이상치여부']=outlier_mask
pp('이상치 후보 수: ', int(df['이상치여부'].sum()))

# 시청분 원본과 보정값 비교
pp(df['시청분'] , df['시청분_보정'])