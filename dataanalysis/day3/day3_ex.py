# day3_ex.py
# 연산자 입출력 형변환 실습

# # 1. 산술 연산자
# a = 10
# b = 3
# print(f'더하기: {a+b}')
# print(f'뺴기: {a-b}')
# print(f'곱하기: {a*b}')
# print(f'나누기: {a/b}') # float
# print(f'몫: {a//b}') # int
# print(f'나머지: {a%b}') # 배수 연산자 사용시 활용
# print(f'거듭제곱: {a**b}')

# # 2. 연산자 우선순위
# # () 가 우선순위가 가장 높음
# # 먼저 연산할 것들은 () 로 묶어줌
# result1 = 2 + 3 * 4 #14
# result2 = (2 + 3) * 4 #20
# print(result1, result2)

# # 3. 비교 연산자 : 결과는 항상 bool
# print(f'10>5 : {10>5}')
# print(f'10<5 : {10<5}')
# print(f'10>=5 : {10>=5}')
# print(f'10<=5 : {10<=5}')
# print(f'10==5 : {10==5}')
# print(f'10<=5 : {10<=5}')
# print(f'10!=5 : {10!=5}')

# # 4. 논리연산자
# age_ok = 22 >= 20 # True
# score_ok = 85 >= 80 # True
# print(f'and : {age_ok and score_ok}') # True
# print(f'or : {age_ok or score_ok}') # True
# print(f'not : {not age_ok}') # False
# a = 5 #0101
# b = 3 #0011
# # 비트 xor => 0110
# print(f'xor: {a ^ b}') #xor : 두비트가 같으면 false(0) 다른면 true(1)
# print(True ^ True) #False
# print(True ^ False) # True
# print(False ^ False) #False
# print(False ^ True)  #True

# # 5. input() 표준입력 함수
# name = input('이름을 입력 하세요: ')
# print(f'입력한 이름: {name}')
# print(type(name))

# # 6. input()으로 입력 받은 숫자의 타입 확인
# age_text = input('나이를 입력 : ')
# print(f'age_text:{age_text}, {type(age_text)}')
# age_int = int(age_text) # 정수 변환
# print(f'age_int:{age_int}, {type(age_int)}')

# # 7. 형변환 실습
# in_int = int(input('정수를 입력 : '))
# in_float = float(input('실수를 입력 : '))
# in_bool = bool(input('불리언 입력(True/False) : '))
# print(type(in_int),type(in_float),type(in_bool))
# str_bool = str(in_bool)
# print(str_bool,type(str_bool))

# # 8. 간단한 가격, 수량 계산
# price = int(input('가격을 입력 :'))
# quantity = int(input('수량 입력 : '))
# total_price = price * quantity # 총액
# print(total_price)
# print(f'총액은 :{total_price:,.0f} 입니다')
# print(f'쉼표 포함 :{total_price:,.0f} 입니다')

# # 9. 할인률을 포함한 주문 계산
# product = input('상품명 입력 :')
# unit_price = int(input('단가 입력 :'))
# qty = int(input('수량 입력 : '))
# discount_rate = float(input('할인률 % 입력 :'))
# subtotal = unit_price * qty
# discount_amount = subtotal * discount_rate/100
# final_amount = subtotal - discount_amount #최종금액
# ****
# print('='*40) #문자열 반복
# print(f'상품명: {product}')
# print(f'할인 전 함계 {subtotal:,.0f}') # 소수점 이하 없이 3자리마다
# print(f'할인 금액 {discount_amount:,.0f}') # 소수점 이하 없이 3자리마다
# print(f'최종 결재 금액 {final_amount:,.0f}') # 소수점 이하 없이 3자리마다
# print('='*40) #문자열 반복

# 10. 형변환 오류 확인
# tc_error1 = int('abc') # Value Error
# tc_error2 = int(35.12) # 데이터 손실 35
# tc_error3 = float(35)  # 35.0




