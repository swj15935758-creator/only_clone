# day4_extra.py
# AI휴먼 Day 4 추가 실습문제

# # 1. 이름 입력 여부 확인
# # 사용자에게 이름을 입력받으세요.
# # 이름이 입력되어 있으면 "이름 입력 완료"를 출력하고,
# # 아무것도 입력하지 않았다면 "이름 없음"을 출력하세요.
# user_name = input('사용자의 이름을 작성 하세요 : ')
# if user_name in '':
#     print('이름 없음')
# else:
#     print('이름입력 완료')
#     print(user_name)

# # 2. 회원등급 확인
# # 회원등급을 입력받으세요.
# # 허용되는 회원등급은 NORMAL, GOLD, VIP입니다.
# # 허용된 등급이면 "정상 등급"을 출력하고,
# # 그 외에는 "입력 오류"를 출력하세요.
# only_meber_grade = ['NORMAL', 'GOLD', 'VIP'] # 회원 등급 3개
# member_grade = input('회원 등급을 입력하세요( NORMAL, GOLD, VIP 중) : ') # 입력층
# if member_grade in only_meber_grade:
#     print('정상 등급')
#     if member_grade == 'NORMAL':
#         print(f'회원의 등급은 : {member_grade}')
#     elif member_grade == 'GOLD':
#         print(f'회원의 등급은 : {member_grade}')
#     elif member_grade == 'VIP':
#         print(f'회원의 등급은 : {member_grade}')
#     else:
#         print('예상치 못한 결과')
# else:
#     print('입력 오류')


# # 3.홀수 / 짝수 판정
# # 정수 하나를 입력받으세요.
# # 짝수이면 "짝수"를 출력하고,
# # 홀수이면 "홀수"를 출력하세요.
#
# ct_number = int(input('숫자를 입력 하세요 홀수 정수 판단 : '))
# if ct_number % 2 == 0: # 2를 나눌때 나머지가 0 이면 짝수
#     print(f' {ct_number} 는 짝수 입니다')
# else:
#     print(f' {ct_number} 는 홀수 입니다')


# # 4. 오전 / 오후 판정
# # 0~23 사이의 시간을 정수로 입력받으세요.
# # 0~11이면 "AM",
# # 12~23이면 "PM",
# # 그 외에는 "입력 오류"를 출력하세요.
#
# hour = int(input('오전/ 오후 판독기 시간 정수 작성(0~23) : '))
# if 0<= hour <12:
#     print('AM')
# elif 12<= hour <=23:
#     print('PM')
# else:
#     print('입력 오류')


# # 5. 계절 판정
# # 월을 1~12 사이의 정수로 입력받으세요.
# # 12, 1, 2월은 "겨울",
# # 3, 4, 5월은 "봄",
# # 6, 7, 8월은 "여름",
# # 9, 10, 11월은 "가을",
# # 그 외에는 "입력 오류"를 출력하세요.
#
# ct_season = int(input("몇월 인지 적어 (1~12) : "))
# if 1<= ct_season <= 12 :
#     print('겨울')
# elif 3<= ct_season <= 5:
#     print('봄')
# elif 6 <= ct_season <=8 :
#     print('여름')
# elif 9 <= ct_season <= 11:
#     print('가을')
# else:
#     print('잘못된 입력')



# # 6. 배송비 판정
# # 구매금액과 회원등급을 입력받으세요.
# # 회원등급은 NORMAL, GOLD, VIP 중 하나입니다.
# # 구매금액이 50,000원 이상이면 "무료배송"을 출력하세요.
# # GOLD 또는 VIP 회원이면서 구매금액이 30,000원 이상이어도 "무료배송"을 출력하세요.
# # 그 외에는 "배송비: 3,000원"을 출력하세요.
# # 회원등급이 잘못 입력되면 "입력 오류"를 출력하세요.
#
# only_member_grade = ['NORMAL', 'GOLD', 'VIP'] # 회원 등급 3개
# product_price = int(input('구매 금액을 입력하세요 단위 (원) :'))# 입력층
# del_price = 3000
# member_grade = input('회원 등급을 입력하세요( NORMAL, GOLD, VIP 중) : ')
#
# if member_grade in only_member_grade:
#     if product_price > 50000:
#         print('무료배송')
#     elif (member_grade == 'GOLD' or 'VIP') and product_price >= 30000:
#         print('무료배송')
#     else:
#         print(f'배송비 : {del_price :,}원 입니다')
# else:
#     print('입력 오류')

# # 7. 장학금 대상 판정
# # 평균점수와 출석률을 입력받으세요.
# # 평균점수가 95점 이상이고 출석률이 85% 이상이면 "우수 장학금 대상"을 출력하세요.
# # 평균점수가 85점 이상이고 출석률이 90% 이상이면 "장학금 대상"을 출력하세요.
# # 그 외에는 "대상 아님"을 출력하세요.
#
# eq_score = int(input('평균 점수를 입력하세요 단위 정수 0~100: ' ))
# attendance = int(input('출석률을 입력하세요 단위(%)정수 0 ~100: '))
#
# if (eq_score < 0 or eq_score > 100) and (attendance < 0 or attendance > 100):
#     print('잘못된 입력')
# elif eq_score >= 95 and attendance >= 85:
#     print('우수 장학금 대상')
# elif eq_score >= 85 and attendance >= 90:
#     print('장학금 대상')
# else:
#     print('대상이 아닙니다')



# # 8. 직원 성과등급 판정
# # 성과점수와 지각횟수를 입력받으세요.
# # 성과점수가 90점 이상이고 지각이 0회이면 S등급,
# # 80점 이상이고 지각이 2회 이하이면 A등급,
# # 70점 이상이고 지각이 4회 이하이면 B등급,
# # 그 외에는 C등급을 출력하세요.
# # 성과점수는 0~100 범위이며 지각횟수는 0 이상이어야 합니다.
# # 잘못된 값이 입력되면 "입력 오류"를 출력하세요.
#
# sus_score = int(input('성과 점수를 입력 하세여 (범위 0~100) :'))
# late_hour = int(input('지각한 횟수를 입력 : '))
# # 지각 횟수 0 보다 작을떄  나 성과 점수가 0이상 100이하 사이가 아닐때 오류
# if (sus_score > 100 or sus_score < 0) or late_hour < 0:
#     print('잘못된 입력')
# elif sus_score >=90 and late_hour == 0:
#     print('S등급')
# elif sus_score >= 80 and late_hour <= 2:
#     print('A 등급')
# elif sus_score >= 70 and late_hour <= 4:
#     print('B 등급')
# else:
#     print('C등급')


# # 9. ATM 출금 검증
# # 현재 잔액과 출금금액을 입력받으세요.
# # 출금금액이 0 이하이면 "잘못된 금액"을 출력하세요.
# # 출금금액이 10,000원 단위가 아니면 "만원 단위로 입력"을 출력하세요.
# # 출금금액이 현재 잔액보다 크면 "잔액 부족"을 출력하세요.
# # 모든 조건을 만족하면 출금 후 잔액을 출력하세요.
#
# my_money = int(input('현재 잔액을 입력하세요 : '))
# out_money = int(input('출금할 금액을 입력하세요 : '))
#
# if my_money <0 :
#     print('잘못된 잔액 입력')
# elif 0 > out_money :
#     print('잘못된 츨금입력')
# elif my_money > out_money :
#     if out_money % 10000 != 0:
#         print('만원 단위로 입력')
#     else:
#         final_money = my_money -out_money
#
# print(f'출금액 : {out_money:,}')
# print(f'잔액 : {final_money:,}')


# 10. 쇼핑몰 할인 계산
# 구매금액, 회원등급, 쿠폰보유 여부를 입력받으세요.
# 회원등급은 NORMAL, GOLD, VIP 중 하나이며 쿠폰보유 여부는 Y 또는 N입니다.
# 구매금액이 100,000원 이상이고 VIP이면 20% 할인,
# 쿠폰이 있고 구매금액이 50,000원 이상이면 15% 할인,
# GOLD 또는 VIP이면서 구매금액이 30,000원 이상이면 10% 할인,
# 구매금액이 30,000원 이상이면 5% 할인,
# 그 외에는 할인을 적용하지 않습니다.
# 여러 조건을 동시에 만족하는 경우 가장 높은 할인율 하나만 적용하고
# 할인율, 할인금액, 최종 결제금액을 출력하세요.

only_member_grade = ['NORMAL', 'GOLD', 'VIP']  # 회원 등급 3개
only_has_coupon = ['Y', 'N']

# 1. 입력 받기 (사용자 편의를 위해 대문자 자동 변환 적용)
buy_price = int(input('구매 금액 입력: '))
member_grade = input('회원등급 입력(NORMAL, GOLD, VIP 중): ')
has_coupon = input('쿠폰 여부(Y or N) 입력: ')

# 오타 방지: 사용자가 안내문대로 NOMAL(R 빠짐) 입력 시 NORMAL로 변경
if member_grade == 'NOMAL':
    member_grade = 'NORMAL'

dc_rate = 0

# 2. 조건 검증 및 할인율 계산
if (member_grade in only_member_grade) and (has_coupon in only_has_coupon) and (buy_price > 0):
    if buy_price >= 100000 and member_grade == 'VIP':
        dc_rate = 20
    elif has_coupon == 'Y' and buy_price >= 50000:
        dc_rate = 15
    elif member_grade in ['GOLD', 'VIP'] and buy_price >= 30000:
        dc_rate = 10
    elif buy_price >= 30000:
        dc_rate = 5
    else:
        dc_rate = 0

    # 3. 결과 출력 (정상 입력 시에만 계산 및 출력)
    dc_money = int(buy_price * dc_rate / 100)  # 할인금액
    total_price = buy_price - dc_money  # 결재 금액

    print(f'할인율: {dc_rate}%')
    print(f'할인금액: {dc_money:,}원')
    print(f'결제금액: {total_price:,}원')

else:
    print('잘못된 입력입니다. 등급, 쿠폰 여부, 금액을 다시 확인해주세요.')






