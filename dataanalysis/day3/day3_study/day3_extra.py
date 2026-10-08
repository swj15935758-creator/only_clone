# day3_extra.pt

# #[문자열 입력] str
# company_name = input("회사명을 입력: ")
# course_name = input("교육과정명 입력: ")

# #[정수입력] int
# participation_member = int(input('참가인원 수 : '))
# client_hour_money = int(input('고객 청구 시간당 교육비(원): '))
# instructor_hour_money = int(input('강사 지급 시간당 강사료(원): '))
# personal_pay_money = int(input('1인당 교재/실습비(원) : '))
# place_equipment_pay_money = int(input('장소 및 장비 비용(원) : '))

# #[실수 입력] float
# total_course_hour = float(input('총 교육시간 : '))
# discount_rate = float(input('할인율(%) : '))

##[입력용]
company_name = input("회사명을 입력: ")
course_name = input("교육과정명 입력: ")
participation_member = int(input('참가인원 수 : '))
total_course_hour = float(input('총 교육시간 : '))
client_hour_money = int(input('고객 청구 시간당 교육비(원): '))
instructor_hour_money = int(input('강사 지급 시간당 강사료(원): '))
personal_pay_money = int(input('1인당 교재/실습비(원) : '))
place_equipment_pay_money = int(input('장소 및 장비 비용(원) : '))
discount_rate = float(input('할인율(%) : '))



# 1교육 판매 금액 int
course_pay_money = int(total_course_hour) * client_hour_money
# 2전체 교재/실습비 int
member_money = participation_member * personal_pay_money
# 3할인전 견젹 금액 int
pre_dc_money = course_pay_money + member_money + place_equipment_pay_money
# 4할인금액 int
dc_money = int(pre_dc_money * discount_rate / 100)
# 5최종 계약 예상금액 int
total_ex_money = pre_dc_money - dc_money
# 6강사비 int
instructor_money = total_course_hour * instructor_hour_money
# 7 총원가 int
total_origin_money = instructor_money + member_money + place_equipment_pay_money
# 8예상이익 int
ex_get_money = total_ex_money - total_origin_money
# 9예상 이익률 float
ex_get_rate = ex_get_money / total_ex_money * 100

# [사업성 판단]
is_profitable = ex_get_money > 0 #돈을 버는가
is_participant_range_ok = 5 <= participation_member <=30 #5이상 30 이하의 인원수인지
is_target_margin_ok = ex_get_rate > 25#예상 이익률이 25% 보다 높은지
can_proceed = is_profitable and is_participant_range_ok and is_target_margin_ok



# 출력 형식지정
print('='*40)
print(f'회사명 :{company_name} ') # str
print(f'교육과정:{course_name}') # str
print(f'참가인원:{participation_member}명') # int
print(f'총 교육시간:{total_course_hour:.1f}시간 \n') #float

print('[견적]')
print(f'교육 판매 금액:{course_pay_money:,}원') # int
print(f'교재/실습비:{member_money:,}원 ') # int
print(f'장소/장비비:{place_equipment_pay_money:,}원') # int
print(f'할인 전 견적금액:{pre_dc_money:,}원 ') # int
print(f'할인률:{discount_rate:,}% ') # float
print(f'할인 금액:{dc_money:,}원 ') # int
print(f'최종 계약 예상 금액:{total_ex_money:,}원 \n') # int

print('[예상 원가 및 손익]\n')
print(f'강사비:{instructor_money:,}원 ') # int
print(f'총 원가:{total_origin_money:,}원 ') # int
print(f'예상 이익:{ex_get_money:,}원 ') # int
print(f'예상 이익률 약:{ex_get_rate:.2f}% \n') # float

print('[사업성 점검]')
print(f'이익 발생 여부 : {is_profitable}')
print(f'권장 인원 충족 여부: {is_participant_range_ok}')
print(f'목표 이익률 충족 여부 : {is_target_margin_ok}')
print(f'사업 진행 기준 충족 : {can_proceed}')

print('='*40)



# 1) 할인율이 커지면 예상 이익과 이익률은 어떻게 변할까요?
# >  둘다 떨어진다

# 2) 참가 인원이 늘어나면 어떤 값들이 함께 변할까요?
# > 강사비 장소 대여 부분은 일정해 인원이 많아질 수록 커진다

# 3) 고객 청구 시간당 교육비와 강사 지급 시간당 강사료의 차이가수익성에 어떤 영향을 줄까요?
# > 차이가 클수록 수익성이 떨어진다  고객의 내는돈이 떨어지거나 강사의 급료가 오르면 수익성이 떨어짐

# 4) 현재 프로그램에서 잘못된 숫자 입력이 들어오면 어떤 문제가 생길까요?
# > value_Error 가 난다

# 5) 다음 수업에서 if 문을 배우면 True/False 결과를 이용해 어떤 메시지를 자동으로 출력할 수 있을까요?
# > 잘못된 값을 넣으면 잘못됬다고 출력이 가능하다 for 문과 융합하면 반복하면서 잘못되면 다시 시도가 가능하다