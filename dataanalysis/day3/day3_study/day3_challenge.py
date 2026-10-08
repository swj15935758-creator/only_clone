# day_3challenge.py
# AI휴먼 Day 3 - Challenge 과제
# 주제: 주문 영수증 계산 + 잘못된 입력 오류 분석
# 권장 시간: 60~80분

# [학습 목표]
# 여러 입력값을 적절한 자료형으로 변환할 수 있다.
# 여러 단계의 금액 계산을 순서대로 구현할 수 있다.
# 중간 계산값을 변수로 분리해 코드의 가독성을 높일 수 있다.
# 숫자가 아닌 입력이 들어왔을 때 발생하는 오류의 원인을 설명할 수 있다.

# [과제 1: 주문 영수증 만들기]
# 아래 정보를 입력받아 최종 결제금액까지 출력하세요.

# 입력 항목
# 상품명
# 단가
# 수량
# 할인율(%)
# 부가세율(%)

print('='*40) #문자열 반복
#입력 항목
product_name = input('상품명을 입력하세요 : ') # 상품명
product_price = int(input('상품의 단가 : '))# 단가
product_amount = int(input('상품의 수량 : '))# 수량
discount_rate = float(input('할인률 (%): ')) #할인률
surtax_rate = float(input('부가세율 (%):')) #부가세율


# 계산식
order_price = product_price * product_amount #주문금액 int
discount_price = order_price * discount_rate / 100#할인금액 float 상태
product_discount_price = order_price - discount_price #할인후 금액 float
suttax = product_discount_price * surtax_rate / 100 # 부가세 float
total_price =  product_discount_price + suttax#최종 결제금액 float

# int 변횐
final_discount_price = int(discount_price) # 할인금액 int
final_product_discount_price = int(product_discount_price) #할인후 금액 int
final_suttax = int(suttax)              #부가세 int
final_total_price = int(total_price) #최종결재 금액 int

#출력 부분
print('='*40) #문자열 반복
print(f'상품명:{product_name} \n 주문 금액 : {order_price:,}원 \n'
      f'할인율 : {discount_rate}% \n 할인 금액 {final_discount_price:,}원 \n'
      f'할인후 금액 {final_product_discount_price:,}원 \n 부가세율 {surtax_rate}% \n'
      f'부가세: {final_suttax:,} 원 \n 최종 결재 금액 : {final_total_price:,}원')

print('='*40) #문자열 반복

# 계산 순서
# 주문금액 = 단가 × 수량
# 할인금액 = 주문금액 × 할인율 ÷ 100
# 할인후금액 = 주문금액 - 할인금액
# 부가세 = 할인후금액 × 부가세율 ÷ 100
# 최종 결제금액 = 할인후금액 + 부가세

# 출력 항목
# 상품명
# 주문금액
# 할인율
# 할인금액
# 할인 후 금액
# 부가세율
# 부가세
# 최종 결제금액

# [과제 2: 오류 상황 관찰]
# 정상 실행을 확인한 뒤, 프로그램을 다시 실행하여 단가 입력란에 abc를 입력해 보세요.

# 아래 질문에 코드 주석으로 답하세요.
# 어떤 오류 이름이 출력되는가?  -> ValueError: invalid literal for int() with base 10: 'abc'
# 왜 이 오류가 발생하는가? -> int 타입이어야 하는데 str 타입의 문자가 와서
# 현재 배운 범위에서 사용자가 지켜야 할 입력 규칙은 무엇인가? -> 숫자로만 적기
# 향후 프로그램을 더 안전하게 만들려면 어떤 기능이 필요할 것 같은가? -> str가 나올때 다시 입력 하는 방법

# [중요]
# 아직 try-except 예외 처리 구현은 필수가 아닙니다.
# 이번 Challenge의 핵심은 오류를 숨기는 것이 아니라, 오류 원인을 읽고 설명하는 것입니다.
# 조건문은 Day 4에서 학습하므로 사용하지 않아도 됩니다.