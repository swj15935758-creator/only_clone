# day3_application.py
# AI휴먼 Day 3 - Application 과제
# 주제: 할인율을 적용한 결제금액 계산기
# 권장 시간: 50~70분
#
# [학습 목표]
# 정수와 실수 입력을 구분해 형변환할 수 있다.
# 여러 단계의 계산 결과를 변수로 나누어 저장할 수 있다.
# 할인율 계산식을 이해하고 구현할 수 있다.
# f-string 숫자 서식을 적용할 수 있다.
#
# [과제]
# 상품 주문 정보를 입력받고 할인율을 적용한 최종 결제금액을 계산하세요.
#
# 입력 항목
# 상품명
# 단가
# 수량
# 할인율(%)
#
# 계산 순서
# 주문금액 = 단가 × 수량
# 할인금액 = 주문금액 × 할인율 ÷ 100
# 최종 결제금액 = 주문금액 - 할인금액

#입력 정보
product = input('상품명을 입력 하세요 : ') # 상품명
price = int(input('입력한 상품의 단가를 입력하세요 : ')) #단가)
amount = int(input('구매할 수량을 입력하세요 : ')) #구매수량
discount_price_rate = float(input('할인률을 입력하세요 : '))  #할인률

#계산식
pre_total_price = price * amount # 주문 금액
discount_price = pre_total_price * discount_price_rate / 100 # 할인 금액 float
total_price = pre_total_price - discount_price # 최종금액 float

#정수 변환
final_total_price = int(total_price) # 최종금액 정수 변환
final_discount_price = int(discount_price) #할인금액 정수 변환

print('='*40) #문자열 반복
print(f'상품명 : {product} \n 주문 금액 : {pre_total_price:,}원 \n 할인율 : {discount_price_rate}% \n '
      f'할인금액: {final_discount_price:,}원 \n 최종 결재 금액: {final_total_price:,}원')
print('='*40) #문자열 반복


# 출력 예시
# 상품명: 모니터
# 주문금액: 540,000원
# 할인율: 10.0%
# 할인금액: 54,000원
# 최종 결제금액: 486,000원
#
# [필수 조건]
# 단가와 수량은 int()로 변환합니다.
# 할인율은 float()로 변환합니다.
# 주문금액, 할인금액, 최종 결제금액을 각각 다른 변수에 저장합니다.
# 금액은 소수점 없이 천 단위 쉼표를 적용합니다.
# 할인율은 소수점 한 자리까지 표시합니다.
# 계산식을 한 줄에 모두 작성하지 말고 처리 단계를 나눕니다.
#
# [추가 확인]
# 할인율 10%를 계산할 때 왜 100으로 나누어야 하는지 주석으로 설명하세요.
# 전체 금액의 10을 곱하면 금액의 10배이고 거기에 100을 나누면 0.1이라는 숫자가 나온다
# 그래서 0.1을 퍼센트로 바꾸면 10% 이고 원래 0.1을 곱하면 되지만 할인률은 상품마다 다르기떄문에
# 할인률을 빼서 계산하기 위해 나눔