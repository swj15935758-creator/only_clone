# day13_basic.py
# 주제:AI휴먼 13일차 Basic 과제 공유오피스 예약 데이터 정제
#
# 아래 데이터를 이용해 공유오피스 예약 데이터를 정제하십시오.
#
import pandas as pd
from python.print_util import pp

df = pd.DataFrame({
    "예약자": [" 김지우 ", "박하준", " 이나연", "최도윤 ", "서윤아", "정민재"],
    "공간": [" Meeting Room ", "MEETING ROOM", "focus room", " Focus  Room ", "Lounge", "LOUNGE "],
    "예약일": ["2026-09-01", "2026/09/02", "2026-09-03", "bad-date", "2026-09-05", "2026/09/06"],
    "회원등급": ["Basic", "Pro", "Basic", "Enterprise", "Pro", "Basic"],
    "사용시간": [2, 3, 1, 2, 4, 18]
})

# 요구사항
# 예약자의 앞뒤 공백을 제거하십시오.
df['예약자']=df['예약자'].str.strip()
# 공간의 앞뒤 공백, 대소문자, 연속 공백을 정리해 모두 소문자로 통일하십시오.
df['공간'] = (
    df['공간']
    .str.replace(r'\s+', ' ')
    # regex=True 앞에껄 정규사용식으로 사용해라 생략해도 정상작동됨 이환경은
    .str.strip()
    .str.lower()
)
# 예약일을 datetime으로 변환하고 실패한 값은 NaT로 처리하십시오.
df['예약일'] = pd.to_datetime( # 날짜 타입으로 변환
    df['예약일'],
    errors='coerce', # 변환 불가시에는 NaT
    format='mixed', # 포맷 = 형식
)

# 예약월, 예약요일 컬럼을 추가하십시오.
df['예약월'] = df['예약일'].dt.strftime('%m')
df['예약요일'] = df['예약일'].dt.day_name()

# 회원등급을 category 자료형으로 변환하십시오.
df['회원등급'] = df['회원등급'].astype('category')

# 사용시간에 대해 IQR 방식의 하한과 상한을 계산하십시오.
q1 = df['사용시간'].quantile(0.25)
q2 = df['사용시간'].quantile(0.5)
q3 = df['사용시간'].quantile(0.75)
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr # 하한, 상한
# IQR 범위를 벗어난 행에 이상치여부=True가 되도록 컬럼을 추가하십시오.
outlier_mask = ~df['사용시간'].between(lower, upper)
df['이상치여부']=outlier_mask
pp(outlier_mask)

# 날짜 변환 실패 건수, 공간 고유값, 이상치 후보 행을 출력하십시오.
pp('날짜 변환 실패 건수',df['예약일'].isna().sum())
pp('고유값',df['공간'].unique())
pp('이상치 후보 행', int(df['이상치여부'].sum()))

# 제출 파일
# day13_basic.py 형식으로 작성한다고 가정하고 문제를 해결하십시오
