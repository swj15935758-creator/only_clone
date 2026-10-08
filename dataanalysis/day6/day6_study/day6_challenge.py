# day6_challenge.py
# AI휴먼 day6 Challenge 과제
# 주제: 함수형 학생 성적 리포트 만들기
# 권장 소요시간: 45~60분
#
# [과제 목표]
# 하나의 프로그램을 역할별 함수로 나눌 수 있습니다.
# 함수의 반환값을 다른 함수의 입력으로 연결할 수 있습니다.
# 리스트, 딕셔너리, 반복문, 조건문을 함수와 통합할 수 있습니다.
#
# [학생 데이터]
# students = [
#     {"name": "김민수", "scores": [85, 90, 78]},
#     {"name": "이서연", "scores": [95, 92, 92]},
#     {"name": "박준호", "scores": [70, 68, 68]},
#     {"name": "최지우", "scores": [82, 88, 91]}
# ]
#
# [등급 기준]
# 90점 이상: A
# 80점 이상: B
# 70점 이상: C
# 60점 이상: D
# 60점 미만: F
#
# [구현 조건]
# 다음 4개의 함수를 작성하세요.
#
# get_average(scores)
# 점수 리스트를 매개변수로 받습니다.
# 반복문으로 합계를 계산합니다.
# 평균을 return으로 반환합니다.
#
# get_grade(score)
# 점수를 매개변수로 받습니다.
# 등급을 A~F 중 하나로 return합니다.
#
# make_report(student)
# 학생 딕셔너리 1개를 매개변수로 받습니다.
# get_average()를 호출합니다.
# 평균값을 get_grade()에 전달합니다.
# "이름 | 평균: 00.0 | 등급: X" 형태의 문자열을 return합니다.
#
# get_class_average(student_list)
# 모든 학생의 개인 평균을 계산합니다.
# 전체 학생의 평균을 return합니다.
#
# [출력 조건]
# 학생별 리포트를 모두 출력합니다.
# 마지막 줄에 전체 학생 평균을 출력합니다.

students = [
    {"name": "김민수", "scores": [85, 90, 78]},
    {"name": "이서연", "scores": [95, 92, 92]},
    {"name": "박준호", "scores": [70, 68, 68]},
    {"name": "최지우", "scores": [82, 88, 91]}
]
#
# def get_average(scores):
#     total = 0
#     for score in scores:
#         total += score
#     return total / len(scores)
#
# def get_grade(score):
#     if score >= 90:
#         return "A"
#     elif score >= 80:
#         return "B"
#     elif score >= 70:
#         return "C"
#     elif score >= 60:
#         return "D"
#     else:
#         return "F"
#
#
# def make_report(student):
#     # 학생의 점수 리스트로 평균 계산
#     avg = get_average(student["scores"])
#     # 계산된 평균값으로 등급 구하기
#     grade = get_grade(avg)
#     # 지정된 서식에 맞추어 문자열 반환 (소수점 첫째 자리 포맷팅)
#     return f"{student['name']} | 평균: {avg:.1f} | 등급: {grade}"
#
#
# def get_class_average(student_list):
#     total_avg = 0
#     # 학생 목록을 반복하며 개인 평균을 누적
#     for student in student_list:
#         total_avg += get_average(student["scores"])
#     # 누적된 합계를 전체 학생 수로 나누어 반환
#     return total_avg / len(student_list)
#
#
#
# # 출력
# # 1. students 리스트를 반복하여 학생별 리포트 출력
# for student in students:
#     print(make_report(student))
#
# # 2. 마지막 줄에 전체 학생 평균 출력 (소수점 첫째 자리 포맷팅)
# class_avg = get_class_average(students)
# print(f"전체 학생 평균: {class_avg:.1f}")

# 강사님 코드
# 성정 리스트 받아서 합계 및 평균 반환
def get_average(scores):
    total = 0 # 합
    for score in scores:
        total += score
    return total / len(scores)

#등급 나누기
def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

# 학생 한명의 출력용 리포트 문자열 만드는 함수
def make_report(student):
    average = get_average(student['scores']) # 평균
    grade = get_grade(average)
    return f"{student["name"]} | 평균: {average:.1f} | 등급: {grade}"

# 전체 학생 평균을 계산하는 함수
def get_class_average(student_list):
    total_average = 0
    for student in student_list:
        averge = get_average(student['scores'])
        total_average += averge
    return total_average / len(student_list) # 전체 학생 평균

# 출력
for student in students:
    print(make_report(student))

print(f'전체 학생 평균 :{get_class_average(students):.1f}')

# [예상 출력]
# 김민수 | 평균: 84.3 | 등급: B
# 이서연 | 평균: 93.0 | 등급: A
# 박준호 | 평균: 68.7 | 등급: D
# 최지우 | 평균: 87.0 | 등급: B
# 전체 학생 평균: 83.2
#
# [설계 의사코드]
# 함수 get_average(scores)
#     합계 계산
#     평균 반환
#
# 함수 get_grade(score)
#     조건에 따라 등급 반환
#
# 함수 make_report(student)
#     student의 점수목록으로 평균 계산
#     평균값으로 등급 계산
#     결과 문자열 반환
#
# 함수 get_class_average(student_list)
#     학생별 평균을 반복 계산하여 누적
#     학생 수로 나누어 반환
#
# students를 반복한다
#     make_report(student) 호출 결과 출력
#
# get_class_average(students) 호출 결과 출력
#
# [완성도 체크]
# 한 함수가 여러 역할을 과도하게 담당하지 않는가?
# 계산 함수는 print보다 return을 활용했는가?
# 함수 이름만 보고 역할을 이해할 수 있는가?
# 평균 함수와 등급 함수를 여러 곳에서 재사용했는가?