# day4_challenge.py

# AI휴먼 Day 4 - Challenge 과제
# 주제: 점수 + 출석률 기반 최종 합격 판정기
#
# [상황]
# 교육과정에서는 성적뿐 아니라 출석률도 함께 반영하여 최종 결과를 판정합니다.
#
# [입력]
# 점수 score: 0~100
# 출석률 attendance: 0~100

# 제작본
score = int(input("점수를 입력하세요(0~100): "))
attendance = int(input("출석를 입력하세요(0~100): "))
if score < 0 or score > 100: # 점수 입력 범위 벗어남
    reason = '입력오류'
    print(f'점수가 0~100 범위를 벗어났습니다 \n 사유 : {reason}')

elif attendance < 0 or  attendance >100: # 출석 입력 범위를 벗어남
    reason = '입력오류'
    print(f'출석률이 0~100 범위를 벗어났습니다 \n 사유 : {reason}')
else:
    if score >= 90 and attendance >= 95:
        result = '우수합격'
        reason = '기준 우수 충족'
    elif score >= 70 and attendance >= 80:
        result = '합격'
        reason = '기준 충족'
    elif attendance < 80:
        result = '불합격'
        reason = '출석률 미달'
    else:
        result = '불합격'
        reason = '출석 미달'
    print(f'점수 : {score}')
    print(f'출석률 : {result}')
    print(f'최종판정 : {reason}')

# # 질문 연습본
# score = int(input("점수를 입력하세요(0~100): "))
# attendance = int(input("출석를 입력하세요(0~100): "))
# if score < 0 or score > 100: # 점수 입력 범위 벗어남
#     reason = '입력오류'
#     print(f'점수가 0~100 범위를 벗어났습니다 \n 사유 : {reason}')
#
# elif attendance < 0 or  attendance >100: # 출석 입력 범위를 벗어남
#     reason = '입력오류'
#     print(f'출석률이 0~100 범위를 벗어났습니다 \n 사유 : {reason}')
# else:
#     if score >= 70 and attendance >= 80:
#         result = '합격'
#         reason = '기준 충족'
#     elif score >= 90 and attendance >= 95:
#         result = '우수합격'
#         reason = '기준 우수 충족'
#     elif attendance < 80: # 출석미달
#         result = '불합격'
#         reason = '출석률 미달'
#     else: # 점수 미달
#         result = '불합격'
#         reason = '점수 미달'
#     print(f'점수 : {score}')
#     print(f'출석률 : {attendance}')
#     print(f'최종판정 : {reason}')

# [판정 규칙]
# 점수 또는 출석률이 0~100 범위를 벗어나면 "입력 오류"를 출력합니다.
# 점수가 90 이상이고 출석률이 95 이상이면 "우수 합격"입니다.
# 위 조건이 아니면서 점수가 70 이상이고 출석률이 80 이상이면 "합격"입니다.
# 출석률이 80 미만이면 "불합격 - 출석률 미달"입니다.
# 그 외에는 "불합격 - 점수 미달"입니다.
#
# [요구사항]
# input(), int(), if, elif, else를 사용합니다.
# and, or를 각각 최소 한 번 사용합니다.
# 조건의 우선순위를 고려하여 작성합니다.
# 판정 결과와 판정 이유가 명확히 보이도록 출력합니다.
#
# [실행 예 1]
# 점수: 95
# 출석률: 97
# 최종 판정: 우수 합격
#
# [실행 예 2]
# 점수: 85
# 출석률: 88
# 최종 판정: 합격
#
# [실행 예 3]
# 점수: 92
# 출석률: 75
# 최종 판정: 불합격 - 출석률 미달
#
# [실행 예 4]
# 점수: 65
# 출석률: 90
# 최종 판정: 불합격 - 점수 미달
#
# [필수 테스트]
# (95, 97), (90, 95), (89, 95), (70, 80), (69, 80), (100, 79), (-1, 90), (80, 101)
#
# [생각해 보기]
# "우수 합격" 조건을 "합격" 조건보다 아래에 작성하면 어떤 문제가 생길까요?
# > 기준 충족 부분이 먼저 실해되어 우수 합격부분의 elif 코드가 실행이 안된다 없는 코드로 봐도 무방하다