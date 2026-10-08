# day2_application.py
# AI휴먼 과정 Day 2 - Application 과제

# [과제명]
# 취업준비생 학습 프로필 카드

# [목표]
# str, int, float, bool, None을 한 프로그램 안에서 구분하여 사용하고 자료형을 점검합니다.

# [권장 시간]
# 35~45분

# [요구사항]
# 다음 변수를 모두 만드세요.
# learner_name: 이름(str)
# age: 나이(int)
# target_job: 희망직무(str)
# python_experience_years: Python 경험기간(float)
# is_job_seeker: 취업준비 여부(bool)
# portfolio_url: 아직 없으면 None
# f-string을 사용해 한 장의 프로필 카드처럼 출력하세요.
# 각 변수의 값을 출력한 뒤 type()으로 자료형도 확인하세요.
# status 변수에 처음 "학습 시작"을 저장한 뒤 "Day 2 완료"로 재대입하고, 변경 전·후 값을 각각 출력하세요.
# 의미가 모호한 a, b, c 같은 변수명은 사용하지 마세요.
# 핵심 코드 줄에 최소 8개 이상의 주석을 작성하세요.
learner_name = '신의진'
age = 25
target_job = 'ai휴먼 서비스 개발자'
python_experience_years = 0.5
study_status = '학습 시작'
is_job_seeker = True
portfolio_url = None
profile_card = f'이름 : {learner_name} \n 나이 : {age} \n 희망직무: {target_job} \n Python 경험 :{python_experience_years} \n 학습 상태 :{study_status} \n취업준비 여부 : {is_job_seeker} \n 포트폴리오 : {portfolio_url}'
print(profile_card)
# print(f'이름 : {learner_name} \n 나이 : {age} \n 희망직무: {target_job} \n Python 경험 :{python_experience_years} \n 변경 전 :{study_status} \n취업준비 여부 : {is_job_seeker} \n 포트폴리오 : {portfolio_url}')

# [출력 예시]
# === AI휴먼 학습 프로필 카드 ===
# 이름: 김AI
# 나이: 24세
# 희망직무: 데이터 분석가
# Python 경험: 0.5년
# 취업준비 여부: True
# 포트폴리오: None

# === 자료형 점검 ===
# learner_name -> <class 'str'>
# age -> <class 'int'>
# ...
print(f'learmer_name -> {type(learner_name)} \n age -> {type(age)}')

# === 상태 변경 ===
# 변경 전: 학습 시작
# 변경 후: Day 2 완료
study_status = 'Day 2 완료'
profile_card = f'\n 이름 : {learner_name} \n 나이 : {age} \n 희망직무: {target_job} \n Python 경험 :{python_experience_years} \n 학습 상태 :{study_status} \n취업준비 여부 : {is_job_seeker} \n 포트폴리오 : {portfolio_url}'
print(profile_card)

# [평가 포인트]
# 서로 다른 자료형을 목적에 맞게 사용했는가?  사용함
# 재대입의 결과를 설명할 수 있는가?           코드한 거는 다를 순 있어도 재대입의 결과는 전에 할당한거 대신 최근에 할당한 것이 들어와서 출력된다
# type() 결과를 보고 각 자료형을 말할 수 있는가?    가능함
# 변수명만 보고 저장된 값의 의미를 추측할 수 있는가?    가능함