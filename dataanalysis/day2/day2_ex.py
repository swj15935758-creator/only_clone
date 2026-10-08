#day2_ex.py
#파이썬 실행 흐름, 변수, 자료형, type()
'''
이 파일은 대부분 주석 처리 그래서 복습할때 번호별로 주석 풀고 다시거는거 확인해야함
'''

# # 1. python 코드 실행 흐름
# print('실습 시작')
# print('Python 코드는 기본적으로 코드의 위에서 아래로 읽어가면서 실행됨')

# # 2. 리터럴과 변수 만들기
# name = '홍길동' # 홍길동이라는 문자열의 타입의 값을 name가 가리킴
# age = 22 # 22이라는 정수 타입의 값을 age에 할당한다
# score = 85.5 # 85.5 라는 정수타입의 값을 score 변수에 할당
# is_job_seeker = True # True 라고 불리는 타입의 값을 is_job_seeker 변수에 할당
# protfolio_url= None# None 아리는 NoneType 값을 portfolio_url 변수에 할당

# # 3. 변수의 값과 타입을 확인
# print(name, type(name))
# print(age, type(age))
# print(score, type(score))
# print(is_job_seeker, type(is_job_seeker))
# print(protfolio_url, type(protfolio_url))

# # 4.변수에 값 재할당
# status = '준비중'
# print(status)
# status = '학습중'
# print(status)

# # 5. 동적 타이핑 ; 실행 시간에 타입이 유동적으로 바뀐다
# data = 100 # 100 이라는 int타입의 값을 data 변수가 할당, data 변수의 타입은 int
# print(data, type(data)) # 100, int
# data = '백' # 백이라는 str 타입의 값을 data 변수가 가리킴 data 변수의 타입은 str
# print(data, type(data))  # 백, str
# data = True #True 라는 bool 타입의 값을 data변수가 가리킴 data변수의 타입은 bool
# print(data, type(data))  # True, bool

# # 6. 변수명은 의미 있게 짓기(매우 중요)
# student_name = '신AI'
# student_age = 25
# desired_job = 'AIHuman 서비스 개발자'
# python_experience_years = 1.5 # 길더라도 의미있는 이름이 좋은 이름
# is_major = False

# # 7. f-string 으로 개인 프로필 출력
# # f-string : 문자열 앞에 f를 사용, 변수의 값이나 연산결과를 포함
#
# student_name = '신의진'
# student_age = 25
# desire_job= 'ai 서비스 개발'
# python_experience_years = 1.5
# is_major = '컴공 소프트'
#
#
# print('\n=== 개인 프로필 ===') # \n : new line 줄바꿈 문자
# print(f'이름: {student_name}')
# print(f'나이{student_age}')
# print(f'희망직무 : {desire_job}')
# print(f'파이싼 경력 년수{python_experience_years}')
# print(f'전공 여부{is_major}')
# print(f'10년 후의 나이{student_age + 10}')
# # print(f' {}')

# # 8. 변수와 값의 참조 (가리킴)
# # 기본 값의 경우는 값복사(value copy) 가 일어남 ; 두 변수에 영향이 없다는 뜻
# first_score = 90
# second_score = first_score  #first_score =90 ,second_score = 90
# print(first_score)
# print(second_score)
#
# second_score = 50 #first_score = 90, second _score = 50
# print(first_score)
# print(second_score)
#
# first_score = 30  # first_score = 30, second_score = 50
# print(first_score)
# print(second_score)

# # 9. 흔한 오류 ;실행 하면서 오류채크 쿠딩중 오류가 날때 다른데 적는게 좋음 : 원인 해결방법 결과 순으로
# 2name = '홍길동' # SyntaxError: invalid decimal literal
# job = AI 개발자 # SyntaxError: invalid syntax
# print(user) # NameError: name 'user' is not defined. Did you mean: 'super'?

# # 10. 상수 (constant)
# # - 상수는 한번 값을 할당하면 항당돤 값을 변경할 수 없는 변수
# # - 상수는 대문자로 만드는 관례가 있음 (암묵적인 룰)
# PI = 3.141592
# print(PI)
# TOTAL_OF_STUDENTS = 100
# print(TOTAL_OF_STUDENTS)

# # 11. extra
# oct_num = 0o10 # 8진수 10
# print(oct_num, type(oct_num)) # 8 <class 'int'>
# hex_num = 0xff
# print(hex_num, type(hex_num))  # 255 <class 'int'>

# 진법, 진수, 진법 변환
# - 진법 : 수를 표현하는 방법
# - 진수 : 진법에 의해 사용되는 수 예) : 0, 1
# 컴퓨터에서는 2, 8, 16 진법을 사용, 일상 생활에서는 10 진법을 사용
# -- bit 라는 정보 차소 단위로 사용하기떄문에 정보 교환시 정해진 단위로 교환 하기 때문에 사용함

# 진법 변환
# 1. 10진수를 다른 진수로 바꿀떄는 계속 진법수로 나눠서 꺼꾸로 쓰기
# 2. 다른 진수를 10진수로 바꿀때는 각 자리수에 진법수 제곱을 모두 더함

# 변환 연습
# 127(8 > 10) 7+16+64 = 87
# 135(7 > 10)5+21+49 = 75
# 10101