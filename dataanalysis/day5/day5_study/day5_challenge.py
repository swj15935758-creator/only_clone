# day5_challenge.pya
# AI휴먼 과정 5일차 Challenge 과제
# 주제: Dictionary 기반 학생 성적표
#
# [목표]
# 학생 이름과 점수를 Dictionary에 저장하고 반복문·조건문을 결합해 학생별 등급과 전체 요약을 출력합니다.
#
# [데이터]
# students = {
#     "민수": 72,
#     "지연": 88,
#     "준호": 95,
#     "서연": 61,
#     "하늘": 84
# }
#
# [요구사항]
# students Dictionary를 그대로 사용합니다.
# items()를 사용해 이름과 점수를 함께 반복합니다.
# 학생별 등급을 다음 기준으로 판정합니다.
# 90점 이상: A
# 80점 이상: B
# 70점 이상: C
# 70점 미만: D
# 80점 이상이면 PASS, 아니면 RETRY도 함께 표시합니다.
# 반복문으로 다음 요약값을 계산합니다.
# 전체 평균
# 합격자 수
# 최고점 학생 이름과 점수
# 학생별 결과와 전체 요약을 보기 쉽게 출력합니다.
# sum(), max()를 사용하지 않고 반복문으로 합계와 최고점을 계산합니다.

# [데이터]
students = {
    "민수": 72,
    "지연": 88,
    "준호": 95,
    "서연": 61,
    "하늘": 84
}



# for name, scores in students.items(): # 등급 매기기 ver1
#     if scores >= 90:
#         grade = "A"
#         is_pass = 'PASS'
#     elif scores >= 80:
#         grade = "B"
#         is_pass = 'PASS'
#     elif scores >= 70:
#         grade = "C"
#         is_pass = 'RETRY'
#     else:
#         grade = "D"
#         is_pass = 'RETRY'
#     print(f"{name}|{scores}점|{grade}등급|{is_pass}")
# print('-' * 30)

# for name, scores in students.items():  # 등급 매기기 ver2
#     if scores >= 80:
#         is_pass ='Pass'
#         if scores >= 90:
#             grade = "A"
#         else:
#             grade = "B"
#     else:
#         is_pass = 'Retry'
#         if scores >= 70:
#             grade = "C"
#         else:
#              grade = "D"
#     print(f"{name}|{scores}점|{grade}등급|{is_pass}")

# 사용할 변수 지정
count = 0 # 총원
score_sum = 0 # 총점
high_score = 0
pass_ct = 0
# print('-' * 30) ver 3
for name, score in students.items():
    # 1. 합격 여부 결정
    if score >= 80:
        is_pass = 'Pass'
        pass_ct +=1
    else:
        is_pass = 'Retry'

    # 2. 학점 등급 결정
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "D"
    if score >= high_score:
        high_score = score
    count += 1
    score_sum += score
    print(f"{name}|{score}점|{grade}등급|{is_pass}")
print(f' 평균: {score_sum / count} 점') #평균 구하기
print(f' 합격자수: {pass_ct} 명')
print(f' 최고 점수: {high_score} 점')

# [출력 예시 형태]
# 민수 | 72점 | C등급 | RETRY
# 지연 | 88점 | B등급 | PASS
# ...
# ------------------------------
# 평균: ...
# 합격자 수: ...
# 최고점: ...
#
# [완료 기준]
# Dictionary의 Key와 Value를 올바르게 처리했습니다.
# 반복문과 조건문을 결합했습니다.
# 합계·합격자 수·최고점이 반복 과정에서 누적 또는 갱신됩니다.
# 학생별 결과와 전체 결과를 구분해서 출력합니다.