# day5_basic.py

# AI휴먼 과정 5일차 Basic 과제
# 주제: 점수 List 순차 처리
#
# [목표]
# List와 for문을 사용해 여러 점수를 하나씩 처리하고 조건문으로 결과를 분류합니다.
#
# [요구사항]
# scores = [72, 88, 95, 61, 83] 리스트를 생성합니다.
# for문으로 scores의 모든 값을 순서대로 출력합니다.
# 각 점수가 80점 이상이면 PASS, 아니면 RETRY를 함께 출력합니다.
# 출력 형식은 아래 예와 비슷하게 구성합니다.
# 72점 : RETRY
# 88점 : PASS
# 전체 코드를 직접 작성하고 핵심 처리 줄에 주석을 작성합니다.

scores = [72, 88, 95, 61, 83]
for score in scores: #scores 안에 있는걸 score 에 하나씩 순서대로 할당 해주는거
    if score >= 80: # 할당 받은걸 80 이상인지 판단하고 PASS or RETRY 를 해주는거
        print(f'{score} : PASS')
    else:
        print(f'{score} : RETRY')

# [완료 기준]
# List를 사용했습니다.
# for문으로 모든 점수를 처리했습니다.
# if/else로 PASS와 RETRY를 구분했습니다.
# 실행 시 오류 없이 5명의 결과가 출력됩니다.