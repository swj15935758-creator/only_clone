from python.print_util import pp
import pandas as pd
df = pd.DataFrame({
    "예약자": [" 김지우 ", "박하준", " 이나연", "최도윤 ", "서윤아", "정민재"],
    "공간": [" Meeting Room ", "MEETING ROOM", "focus room", " Focus  Room ", "Lounge", "LOUNGE "],
    "예약일": ["2026-09-01", "2026/09/02", "2026-09-03", "bad-date", "2026-09-05", "2026/09/06"],
    "회원등급": ["Basic", "Pro", "Basic", "Enterprise", "Pro", "Basic"],
    "사용시간": [2, 3, 1, 2, 4, 18]
})


# 1. 문자열 정제
df['예약자'] = df['예약자'].str.strip()
df['공간'] = (
    df['공간']
    .str.strip()
    .str.lower()
    .str.replace(r'\s+',' ',regex=True) # 공백 문자가 1개 이상이면 1개로
)

# 2. 날짜 변환, 파생 변수 생성
df['예약일'] = pd.to_datetime(
    df['예약일'],
    errors='coerce', # 블가시NaT
    format = 'mixed'
)

df['예약월'] = df['예약일'].dt.month
df['예약요일'] = df['예약일'].dt.day_name()

# 3. 범주형 자료형 변환
df['회원등급'] = df['회원등급'].astype('category')

# 4. IQR 이상치 탐지
q1 = df['사용시간'].quantile(q=0.25) # 1 사분위 수, 1/4
q3 = df['사용시간'].quantile(q=0.75)  # 3 사분위 수, 3/4
iqr = q3 - q1 # 중앙 50% 범위
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
# 사용 시간이 lower ~ uper 가 아닌것은 true
df['이상치여부'] = ~df['사용시간'].between(lower, upper) #이상치 여부


# 결과 확인
pp('날짜 변환 실패 건수 : ',df['예약일'].isna().sum())
pp('공간 고유값', sorted(df['공간'].unique()))
pp(f'IQR 하한={lower:.2f}, 상한={upper:.2f}')
pp(df.loc[df['이상치여부'],['예약자','사용시간','이상치여부']])
pp(df)




























