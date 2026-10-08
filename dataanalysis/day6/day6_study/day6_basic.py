# day6_basic.py
# AI휴먼 day6 Basic 과제
# 주제: 두 수를 더해 반환하는 함수
# 권장 소요시간: 25~35분
#
# [과제 목표]
# 함수를 직접 정의할 수 있습니다.
# 매개변수와 인수를 구분할 수 있습니다.
# 계산 결과를 print()가 아닌 return으로 반환할 수 있습니다.
#
# [문제]
# 다음 조건을 만족하는 프로그램을 작성하세요.
#
# add_numbers(a, b) 함수를 작성합니다.
# 함수는 두 수 a와 b를 더한 결과를 return으로 반환합니다.
# 함수 안에서는 결과를 출력하지 않습니다.
# 아래 세 번의 함수 호출 결과를 각각 출력합니다.
# add_numbers(10, 20)
# add_numbers(3, 7)
# add_numbers(-5, 8)
# 각 핵심 코드 줄에 이해하기 쉬운 주석을 작성합니다.

def add_numbers(num1, num2):
     result = num1 + num2
     print(result)

add_numbers(10, 20)
add_numbers(3, 7)
add_numbers(-5, 8)


# [예상 출력]
# 30
# 10
# 3
#
# [의사코드]
# 함수 add_numbers(a, b)
#     result = a + b
#     result를 반환한다
#
# 10과 20을 전달하고 결과 출력
# 3과 7을 전달하고 결과 출력
# -5와 8을 전달하고 결과 출력
#
# [체크리스트]
# def를 사용했는가?
# 매개변수 a, b를 사용했는가?
# return을 사용했는가?
# 함수 호출 결과가 예상값과 같은가?