# day6_application.py
# AI휴먼 day6 Application 과제
# 주제: 성적 등급 판정 로직을 함수로 분리하기
# 권장 소요시간: 35~45분
#
# [과제 목표]
# 조건문을 함수로 분리할 수 있습니다.
# 반환값을 반복문과 결합할 수 있습니다.
# 리스트와 딕셔너리에 저장된 데이터를 함수로 처리할 수 있습니다.
#
# [문제]
# 다음 학생 데이터를 사용하여 학생별 등급을 출력하는 프로그램을 작성하세요.
#
# students = {
#     "김민수": 87,
#     "이서연": 95,
#     "박준호": 73,
#     "최지우": 61,
#     "정하늘": 55
# }
#
# [등급 기준]
# 90점 이상: A
# 80점 이상: B
# 70점 이상: C
# 60점 이상: D
# 60점 미만: F
#
# [구현 조건]
# get_grade(score) 함수를 작성합니다.
# get_grade 함수는 점수를 받아 A~F 중 하나를 return으로 반환합니다.
# students 딕셔너리를 반복문으로 처리합니다.
# 학생 이름, 점수, 등급을 한 줄씩 출력합니다.
# 함수 안에서 학생 이름을 직접 사용하지 않습니다.
# 등급 판정은 반드시 get_grade 함수에 맡깁니다.

students = {
    "김민수": 87,
    "이서연": 95,
    "박준호": 73,
    "최지우": 61,
    "정하늘": 55
}

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

# 아이템 들에서 이름과 점수 순회
for name, score in students.items():
    get_grade(score)
    print(f'{name} | {score} | {get_grade(score)}')

# [예상 출력]
# 김민수 | 87점 | B등급
# 이서연 | 95점 | A등급
# 박준호 | 73점 | C등급
# 최지우 | 61점 | D등급
# 정하늘 | 55점 | F등급
#
# [의사코드]
# 함수 get_grade(score)
#     score가 90 이상이면 A 반환
#     아니고 80 이상이면 B 반환
#     아니고 70 이상이면 C 반환
#     아니고 60 이상이면 D 반환
#     그 외에는 F 반환
#
# students를 반복한다
#     현재 학생의 점수로 get_grade 호출
#     이름, 점수, 반환받은 등급 출력
#
# [추가 확인]
# get_grade(90)은 A인가?
# get_grade(80)은 B인가?
# get_grade(60)은 D인가?
# get_grade(59)는 F인가?