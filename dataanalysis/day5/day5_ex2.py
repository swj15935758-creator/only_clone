#day_ex2.py
# 파이썬 타입 정리
#  primitive type (Scallar type) : 하나의 변수에 하나의 데이터를 저장
#                                  정수 실수 물자열 불리언 NoneType
#complex type : 하나의 변수에 여러 데이터를 저장
#               리스트, 튜플, 딕셔너리, 셋, 클래스
# mutable type : 값을 변경할 수 있는 타입
#                리스트, 딕셔너리, 셋, 클래스
#immutable type : 값을 변경 할 수 없는 타입, 딕셔너리 키는 immutable 해야함
#                 정수, 실수, 문자열, 불리언, 튜플

# 정수
print(type(100)) #<class 'int'>
# 실수
print(type(3.14))# <class 'float'>
# 문자열
print(type('hello')) # <class 'str'>
# 불리언
print(type(True)) # <class 'bool'>
# NoneType
print(type(None)) #<class 'NoneType'>
# 리스트(list, [])
# 1. 순서대로 요소를 저장
# 2. 어떤 타입의 요소도 저장
# 3. mutable 타입으로 값의 변셩, 추가 , 삭제 가능
# 4. 중복 요소 저장 가능

print(type([1,2,3,])) #<class 'list'>

# 튜플 (tuple, ())
#  1. 기본적으로 리스트의 특성을 가짐
#  2. immutable 타입으로 값의 변경, 추가, 삭제 불가
print(type((1,2,3,)))  # <class 'tuple'>

# 딕셔너리(dictionary, {})
# 1. 아이템(키:값) 순서가 없음
# 2. 키는 immutable 타입이어야 함, 값은 상관 x
# 3. 키는 중복 불허 : 값을 구별 할 방법이 없음, 값은 중복 허용
print(type(({'name':'John', 'age':25, 'city':'New York' })))  # <class 'dict'>

# 셋 (set, {})
# 1. 요소의 순서가 없음
# 2. 중복데이터틑 한번만 저장 : 리스트의 중복 제거에 많이 사용
print(type(set())) # <class 'set'>

# question : {}는 => dictionary ; Empty dict
print(type({}))
























