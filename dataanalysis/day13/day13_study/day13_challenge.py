# day13_challenge.py
# 주제:AI휴먼 13일차 Challenge 과제
# 주제: 스마트팩토리 설비 센서 데이터 정제 파이프라인

import pandas as pd

from python.print_util import pp

df = pd.DataFrame({
    "설비ID": [" mx-01 ", "MX-01", "mx-02", " MX-02 ", "MX-03", "mx-03", "MX-04", "mx-04"],
    "점검시각": ["2026-09-01 08:30", "2026/09/01 12:30", "2026-09-02 09:00", "invalid", "2026-09-03 10:10", "2026/09/03 16:20", "2026-09-04 07:50", "2026-09-04 18:10"],
    "상태": [" normal ", "NORMAL", "Warning", " warning", "normal", "ALERT", "alert ", "Normal"],
    "온도": [62.1, 63.0, 64.2, 63.8, 65.1, 64.7, 66.0, 142.0],
    "진동": [1.2, 1.3, 1.4, 1.5, 1.2, 1.6, 1.4, 8.9]
})

# 요구사항
# 반복되는 정제 규칙을 함수로 작성하십시오.

# clean_text(series): 앞뒤 공백 제거, 연속 공백 정리, 소문자 변환
def clean_text(series):
    return (
        series.astype('str')
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.lower()
    )

# iqr_bounds(series): IQR 하한과 상한 반환
def iqr_bounds(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr

# 설비ID는 공백 제거 후 대문자로 통일하십시오.
df['설비ID'] = df['설비ID'].str.strip().str.upper()

# 상태는 normal, warning, alert로 통일하십시오.
df['상태'] = clean_text(df['상태'])

# 점검시각을 datetime으로 변환하고 실패한 값은 NaT로 처리하십시오.
df['점검시각'] = pd.to_datetime(
    df['점검시각'],
    errors='coerce',
    format='mixed',
)

# 점검일, 점검시간, 점검요일 파생 컬럼을 만드십시오.
df['점검일'] = df['점검시각'].dt.strftime('%Y-%m-%d')
df['점검시간'] = df['점검시각'].dt.strftime('%H:%M')
df['점검요일'] = df['점검시각'].dt.day_name()

pp(df[['점검시각', '점검일', '점검시간', '점검요일']])

# 상태를 normal < warning < alert 순서의 순서형 category로 만드십시오.
progress_type = pd.CategoricalDtype(
    categories=['normal', 'warning', 'alert'],
    ordered=True
)
# 온도와 진동 각각에 대해 IQR 하한/상한을 계산하십시오.
tem = iqr_bounds(df['온도'])# 온도
pp(tem)
viv = iqr_bounds(df['진동'])# 진동
pp(viv)
# 각 값이 IQR 범위를 벗어나면 온도이상, 진동이상 컬럼에 True를 기록하십시오.
# 하나라도 이상하면 센서이상=True가 되도록 컬럼을 만드십시오.
# 원본 센서값은 보존하고 온도_보정, 진동_보정을 clip()으로 만드십시오.
# 다음 품질 점검 결과를 딕셔너리 quality_report로 작성해 출력하십시오.
# 전체 행 수
# 날짜 변환 실패 수
# 상태 범주 목록
# 온도 이상치 수
# 진동 이상치 수
# 하나 이상의 센서 이상 행 수
# 최종적으로 설비ID, 점검시각, 상태, 원본 센서값, 보정 센서값, 이상 여부를 출력하십시오.
#
# 추가 조건
# 이상치 행을 삭제하지 마십시오.
# 정제 전 원본값을 확인할 수 있도록 센서 원본 컬럼은 덮어쓰지 마십시오.

