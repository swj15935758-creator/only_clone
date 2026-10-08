# day5_application.py

# AI휴먼 과정 5일차 Application 과제
# 주제: 반복문 기반 성적 요약
#
# [목표]
# 점수 List를 반복하면서 합격자 수, 평균, 최고점을 직접 계산합니다.
#
# [데이터]
# scores = [72, 88, 95, 61, 83, 90]
#
# [요구사항]
# for문을 사용해 전체 점수 합계를 계산합니다.
# 80점 이상인 합격자 수를 계산합니다.
# 평균 점수를 계산해 소수점 둘째 자리까지 출력합니다.
# 최고점을 반복문과 비교 조건으로 직접 찾습니다.
# 다음 정보를 마지막에 출력합니다.
# 전체 학생 수
# 점수 합계
# 평균 점수
# 합격자 수
# 최고점
# sum(), max()를 사용하지 않고 반복문으로 계산합니다.
scores = [72, 88, 95, 61, 83, 90]
ct_score = 0
number_hap = 0
max_score = 0
count_st = 0
for ct in scores: #전체 학생수
    count_st += 1


for score in scores: # 점수 합 구하기
    number_hap += score


for score in scores: # 80이상인 인원 새기
    if score >= 80:
        ct_score += 1

for score in scores: # 최고점 찾기
    if score > max_score:
        max_score = score

vt_score = number_hap / len(scores) # 평균점수 구하는 식


print(f'총 학생수  {count_st}') #총 학생수
print(f'총점수: {number_hap}')
print(f'평균 점수: {vt_score:.2f} 점')
print(f'80점 이상인 합격자수 {ct_score}') # 80 이상인 합격자수
print(f'최고점수: {max_score} 점')




# [완료 기준]
# 누적 변수(total, pass_count 등)를 반복문 밖에서 초기화했습니다.
# 반복문에서 각 점수를 빠짐없이 처리했습니다.
# 계산 결과가 논리적으로 맞습니다.
# 코드 흐름을 입력 → 반복 → 조건 → 누적 → 출력 순서로 설명할 수 있습니다.