# day2_basic.py
# AI휴먼 과정 Day 2 - Basic 과제
#
# [과제명]
# 나의 기본 프로필 출력 프로그램
#
# [목표]
# 변수에 값을 저장하고 print()와 f-string으로 출력하는 기본 흐름을 익힙니다.
#
# [권장 시간]
# 20~30분
#
# [요구사항]
# 다음 4개의 변수를 만드세요.
# name: 자신의 이름, str
# age: 자신의 나이, int
# desired_job: 희망직무, str
# course_name: "AI휴먼", str
# 각 변수에 알맞은 값을 저장하세요.
# 아래 형식과 비슷하게 f-string으로 출력하세요.
# 마지막에 name과 age의 자료형을 type()으로 확인하세요.
# 핵심 코드 줄에 최소 5개 이상의 쉬운 주석을 작성하세요.
name = '신의진'
age = 25
desired_job = 'ai휴먼 서비스 개발'
course_name = "AI휴먼"
print(f'이름 : {name} \n 나이 : {age} \n 희망 직무 : {desired_job} \n 수강 과목 : {course_name} \n name 자료형 : {type(desired_job)} \n age 자료형 : {type(age)}')

# [출력 예시]
# === 나의 기본 프로필 ===
# 과정명: AI휴먼
# 이름: 홍길동
# 나이: 22세
# 희망직무: AI 개발자
# name 자료형: <class 'str'>
# age 자료형: <class 'int'>
#
# [제출 체크]
# 실행 오류가 없는가?               없음
# 변수명이 의미를 잘 나타내는가?     잘 나타냄
# 문자열에는 따옴표를 사용했는가?    사용했음
# 나이는 int로 저장했는가?           저장했음
# type() 결과를 확인했는가?         확인했음