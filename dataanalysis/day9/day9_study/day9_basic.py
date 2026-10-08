# day9_basic.py
# 주제:AI휴먼 9일차 Basic 과제
# 주제: 1차원 NumPy 배열 기초 분석
#
# [상황]
# 고객센터에서 한 시간 동안 처리한 8건의 상담 대기시간(분)을 다음과 같이 기록했습니다.
#
# 12, 8, 15, 6, 20, 9, 11, 7
#
# [요구사항]
# 위 데이터를 NumPy 1차원 배열로 생성하세요.
# 배열의 shape, ndim, size, dtype을 각각 출력하세요.
# 전체 대기시간의 합계, 평균, 최솟값, 최댓값을 출력하세요.
# 평균 대기시간보다 긴 데이터만 조건 인덱싱으로 추출하세요.
# 모든 대기시간이 2분씩 감소했다고 가정하고 벡터 연산으로 개선 후 배열을 출력하세요.
# 개선 후 평균 대기시간을 출력하세요.
#
# [조건]
# Python 리스트 반복문으로 합계나 평균을 직접 계산하지 않습니다.
# NumPy 배열 연산과 집계 메소드를 사용합니다.
import numpy as np
rating_hours = np.array([12,8,15,6,20,9,11,7])
#shape 배열의 형태
print(rating_hours.shape)
#ndim 차원수
print(rating_hours.ndim)
#size 원소 개수
print(rating_hours.size)
#dtype 자료형
print(rating_hours.dtype)

#전체 합계
print(rating_hours.sum())
# 평균
print(rating_hours.mean())
# 최솟값
print(rating_hours.min())
#최댓값
print(rating_hours.max())

# 평균 시간 보다 긴서 출력
avg_high = rating_hours > rating_hours.mean()
print(avg_high)
# 숫자로 출력
print(rating_hours[avg_high])

# 2분 삼소 가정
print(rating_hours - 2)

# 개선후 평균
nice_rating_hours = rating_hours - 2
print(nice_rating_hours.mean())




