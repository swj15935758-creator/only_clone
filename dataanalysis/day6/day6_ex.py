#day6_ex.py
# function, parameter, argument, return, score, ........

# # 1. 함수 정의 / 호출
# def say_hello():
#     print('안녕 나야 AI 휴먼')
#     # return None 이 생략된것
# # 함수호출
# say_hello()
#
# # 2. 매개변수와 인수 인자
# def greet(name):
#     print(f'{name}님 안녕 하신가')
# greet('신의진')
# greet('박세정')
# greet('이스트 학습 튜터')

# # 3. 여러 매개 변수와 return
# def add(a,b):
#     result=a+b
#     return result # 값을 리턴할 때는 return 생략 불가 생략은 None 이기 떄문
# sum_result=add(10,20)
# print(f'10 + 20 = {sum_result}')

# # 4. print()  와 return 의 차이
# def add_print(a, b):
#     print(a+b)
# def add_return(a, b):
#     return a+b
# add_print(10, 20)
# return_value = add_return(10, 20)
# print(f'반환 값 {return_value}')

# # 5. 위치 인수와 키워드 인수
# def introduce(name, job):
#     print(f'이름: {name} 희망직무 : {job}')
# introduce('박준호', 'AI개발자')
# introduce(job='데이트 분석가', name='김땡땡')

# # 6. 기본값 매개변수
# # message 파라미터에 인수 전달이 안되면 환영 합니다
# def welcome(name, message = '환영해라'):
#     print(f'{name}님 {message}')
# welcome('김하늘') # message = '환영해라'
# welcome('신의진','신병 받아라') # message = '신병 받아라'

# # 7. 조건문을 함수로 분리
# def get_grade(score):
#     if score >= 90:
#         return 'A'
#     elif score >= 80:
#         return 'B'
#     elif score >= 70:
#         return 'C'
#     elif score >= 60:
#         return 'D'
#     else:
#         return 'F'
#
# grade = get_grade(87) #B
#
# test_scores = [95,84,76,59]
# for score in test_scores:
#     current_reade = get_grade(score)
#     print(f'{score}점 > {current_reade}등급')

# # 8. 리스트를 매개 변수로 전달 받아 평균 구하기
# def get_average(scores):
#     total = 0
#     for score in scores:
#         total += score
#     return total/len(scores)
# my_scores= [85,90,78]
# my_average = get_average(my_scores)
# print(f'평균 : {my_average:.1f}')
#
# my_grade = get_grade(my_scores) #평균으로 등급 계산
# print(f'등급: {my_grade}')
#
# # 9. 여러 값을 반환
# def get_total_average(score1, score2):
#     total = score1 + score2
#     average = total / 2
#     return total, average # 2개 값 반환
# #반환된 2개의 값을 각변수에 할당 (unpaking, 구조분해 할당)
# total_score, average_score = get_total_average(88,92)
#
# print(f'총점: {total_score},평균:{average_score:.1f}')

# # 10. 전역 변수의 변경은 함수내에서 하지 않도록
# # Why?  외부 스코프의 변수값에 내부 스코프가 영향을 주는건 좋지 않음
# #       명확한 스코프 분리가 모듈화에 유리
#
#
# # count : increase 함수의 지역변수
# # count 는 increase 함수가 호출되어야 메모리에 생성
# # increase 함수가 retrun 하면 메모리에 제거됨
# # 즉 count 는 외부 전역변수의 값에 영향x
# # 이런 함수를 Pure Function
# # 순수함수로 프로그래밍 하는 기법을 함수형 프로그래핑이라 함
# def increase(count):
#     return count +1
# # 전역변수
# current_count = 0
#
# current_count = increase(current_count)
# current_count = increase(current_count)
# current_count = increase(current_count)
#
# print(f'current_count = {current_count}')




# [변수의 스코프(scope)]
# 	- 스코프 : 변수를 참소(사용)할 수 있는 범위
# 	- 파이썬은 전역(global) 스코프 지역(local) 스코프를 사용
# 	- 전역 스코프 : 함수 밖에서 정의 해서 코드 어디에서나 참조 가능
# 	- 지역 스코프 : 함수 내에서 정의 해서 함수가 호출될떄 메모리에 생성되고
# 			함수가 리턴하면 메모리에서 사라짐, 함수 내에서 참조 가능
# 	- 전역스코프와 지역스코프에 동일한 이름의 변수, 함수가 있다면
# 	- 지역 스코프에 있는 것이 우선함(지역변수가 전역변수를 shadowing 했다고 함)
# 	- LEGB (Local, Encosing, Global, Built-in)
# 	- LEGB :파이썬이 변수를 찾는 순서 (Local > EnClosing > Global > Buint-in)
# 	- Local : 함수내부
# 	- EnClosing : 함수를 감싸고 있는 함수 내부(파이썬 함수내에 함수를 정의하는게 가능)
# 	- Global : 함수 외부
# 	- Built-in : 파이썬이 제공하는 전역 함수 영역

# x = 100 # 전역변수
# def outer(): # outer(enclosing) function
# 	y=200 # outer function의 지역 변수
# 	def inner(): #inner(nested) function
# 		z = 300 # inner function 의 지역변수
# 		print(z)
# 		print(y)
# 		print(x)
# 	inner()
# outer()
#
# # 클로져 (closure)
# # 외부함수가 종료되면 외부 함수에서 저의한 변수가 메모리에서 사라져야 함
# # 외부함수 내에서 내부함수를 저의하고 내부 함수가 외부함수의 에서 정의한 변수를
# # 리턴하게 만들어서 외부함수가 종료 되었음에서 외부함수에서 정의한 변수를
# # 계속 사용할수 있게됨 (또는 계속 사용할수 있게 해주는 내부 함수
# # 목적: 함수 내부에 변수를 상성하고 외부에서 그 변수의 값을 임의 변경하는 것을 막을의도
# # => 캡슐화(Encapsulation) 또는 정보 은닉(information hinding)
# def outer():
# 	x = 10 # outer 함수의 지역변수
# 	def inner(): # inner 함수에서 outer 함수의 변수를 사용
# 		print(x)
# 	return inner # inner 함수를 리턴
# func = outer()
#
# func() #10, x 변수가 살아있음!
#
# # 람다함수(lambda function)
# # 	- 이름이 없는 익명 함수로 주로 일회성으로 기능을 생성해 사용할 목적으로 생성
# #	- 문법: lambda 파라미터리스트 : 리턴값
# #	- 람다 함수는 값(리터럴) 이름로 다른 함수에 인자로 전달 가능
# #	- 리스트의 요소나 딕셔너리의 값으로 사용 가능
# #	- 함수의 리턴 값으로 사용 가능
#
# # 익명의 람다 함수를 생성해 squarex 변수가 가리키게 함
# # 람다 함수의 이름은 내부적으로 정해지고 개발자가 알지 못함
# squarex = lambda x : x**2
# print(squarex(5)) # 25

# # 람다 함수를 사용해 리스트 정렬
# students = [
# 	('철수' ,85),
# 	('영희' ,92),
# 	('민수' ,78),
# 	('지영' ,90)
# ]
#
# students_asc = sorted(students, key=lambda x : x[1]) # 이터러블, 정렬 기준
# print(students)
# print(students_asc)
#
# students_asc = sorted(students, key=lambda x : x[1], reverse = True) # reverse : True 내림차순 정렬
# print(students)
# print(students_asc)


# 고차함수, 콜백함수
# 고차함수(High-order function) : 함수 인자를 전달 받거나, 함수를 리턴하는 함수
# 콜백 함수(call-back function) : 함수에 인자로 전달되는 함수

# map(람다함수, 이터러블) 고차함수 : 이터러블의 각 요소에 람다함수를 적용하는 함수
# 고차함수 : map, 콜백함수: 람다함수
scores = [90,85,75]
new_scores = list(map(lambda x : x+10,scores))
print(new_scores)

# 고차함수
def calc(a,b,f): # 2개의 값, 1개의 함수
	return  f(a,b) # 2개의 값을 인자로 하는 함수의 실행 결과를 리턴
print(calc(3,5, lambda a,b: a+b))
print(calc(3,5, lambda a,b: a-b))
print(calc(3,5, lambda a,b: a*b))
print(calc(3,5, lambda a,b: a/b))


# filter(람다 함수 이터러블) 고차함수
# : 이터러블의 각 요소 중 람다 함수 조건에 맞는 요소를 추출하는 함수
# 고차함수 filter: 콜백함수 : 람다함수
scores = [90,85,75]
new_scores = list(filter(lambda x : x>80, scores))
print(new_scores)



















