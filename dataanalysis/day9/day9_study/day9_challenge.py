# day9_challenge.py
# 주제:AI휴먼 9일차 Challenge 과제
# 주제: 브로드캐스팅과 조건 인덱싱을 활용한 생산라인 품질 분석
#
# [상황]
# 4개 생산라인에서 6시간 동안 집계한 시간당 불량 개수는 다음과 같습니다.
# 각 행은 생산라인 1~4, 각 열은 1~6시간 구간을 의미합니다.
#
# 라인 1: 3, 5, 4, 6, 2, 4
# 라인 2: 6, 7, 5, 8, 6, 7
# 라인 3: 2, 3, 1, 4, 3, 2
# 라인 4: 4, 5, 6, 5, 7, 4
#
# 각 라인의 시간당 목표 불량 개수는 다음과 같습니다.
# 라인 1: 4개, 라인 2: 5개, 라인 3: 3개, 라인 4: 4개
#
# [요구사항]
# 1. 불량 데이터를 4행 6열 NumPy 배열로 생성하세요.
import numpy as np
line_falty_amount = np.array(
    [
    [3,5,4,6,2,4], # 라인1
    [6,7,5,8,6,7], # 라인2
    [2,3,1,4,3,2], # 라인3
    [4,5,6,5,7,4]  # 라인4
    ]
)
# 2. 각 라인의 평균 불량 개수를 계산하세요. 각 라인 평균 불량을 4개로 나눔
print('[라인별 평균 불량 갯수]')
avg_falty_amount1,avg_falty_amount2,avg_falty_amount3,avg_falty_amount4 = line_falty_amount.mean(axis=1)
print(f'라인1:{avg_falty_amount1}'
      f'\n라인2:{avg_falty_amount2}'
      f'\n라인3:{avg_falty_amount3}'
      f'\n라인4:{avg_falty_amount4}')
print('='*40)
# 3. 각 시간대의 전체 불량 개수를 계산하세요. 시간대 별로 불량 개수를 함
hour_1,hour_2,hour_3,hour_4,hour_5,hour_6= line_falty_amount.sum(axis=0)
lines_faulty_hour = hour_1,hour_2,hour_3,hour_4,hour_5,hour_6
print('[시간대별 나오는 불량품]')
print(f'1시간대:{hour_1}\n'
      f'2시간대:{hour_2}\n'
      f'3시간대:{hour_3}\n'
      f'4시간대:{hour_4}\n'
      f'5시간대:{hour_5}\n'
      f'6시간대:{hour_6}')
# 4. 각 라인의 목표값을 1차원 배열 [4, 5, 3, 4]로 생성하세요.
lines_purpose_value = np.array([4,5,3,4])
# print(lines_purpose_value)

# 5. np.newaxis를 사용해 목표값 배열을 (4, 1) 형태로 변경하세요.
new_lines_purpose_value = lines_purpose_value[np.newaxis].T#축 추가
# print(new_lines_purpose_value) #바뀐지 확인

print('='*40)

# 6. 브로드캐스팅으로 실제 불량 개수 - 라인별 목표값 차이 배열을 계산하세요.
reality_line1,reality_line2,reality_line3,reality_line4 = lines_faulty_hour - new_lines_purpose_value
reality_lines = line_falty_amount - new_lines_purpose_value
print('[라인별 시간대 마다 실제 불량 갯수]')
print(f'라인 1 :{reality_line1}\n'
      f'라인 2 :{reality_line2}\n'
      f'라인 3 :{reality_line3}\n'
      f'라인 4 :{reality_line4}')

print('='*40)

# 7. 목표값을 초과한 위치만 Boolean 배열로 표시하세요.
print('[목표값 초과 bool 표]')
is_lines = reality_lines > 0
print(is_lines)

# 8. 목표 초과 횟수를 라인별로 계산하세요.
over_count = is_lines.sum(axis=1)
print('='*40)
print(f'[라인별 초과횟수]'
      f'\n라인1:{over_count[0]}'
      f'\n라인2:{over_count[1]}'
      f'\n라인3:{over_count[2]}'
      f'\n라인4:{over_count[3]}')

print('='*40)

# 9. 목표 초과 횟수가 가장 많은 라인의 인덱스를 찾으세요.
print(f'초과 횟수가 가장 많은 라인 인덱스 : {np.argmax(over_count)}') #라인 1이라는 뜻

print('='*80)

# 10. 각 라인 안에서 불량 개수를 0~1 범위로 Min-Max 정규화하세요.
#  공식: (값 - 라인별 최솟값) / (라인별 최댓값 - 라인별 최솟값)
lines_min = line_falty_amount.min(axis=1)[:, np.newaxis] # 최소값의 새로운 축을 추가 하면서 4행으로
lines_max = line_falty_amount.max(axis=1)[:, np.newaxis] # 최대값의 새로운 축을 추가 하면서 4행으로
normalization_line_fault_amount = (line_falty_amount - lines_min) / (lines_max - lines_min)

# 11. 정규화 과정에서는 라인별 최솟값과 최댓값의 shape가 브로드캐스팅에 맞도록 (4, 1)이 되게 처리하세요.
print('[정규 분포표]')
print(normalization_line_fault_amount)
print('='*80)

# [조건]
# 라인별 집계에는 axis=1, 시간대별 집계에는 axis=0을 사용합니다.
# 목표값 비교와 정규화에서 반복문을 사용하지 않습니다.
# np.newaxis 또는 동등한 reshape 방식을 사용해 브로드캐스팅 구조를 직접 구성합니다.
