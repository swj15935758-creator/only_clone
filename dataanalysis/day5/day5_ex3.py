# # day5_ex3.py
#
# # # 리르스, 딕셔너리, 셋 주요 메소드
# #
# # # 1. list의 주요 메소드
# # fruits = ['apple','banana','orange']
# # print(fruits)
# #
# # fruits.append('grape') # 요소를 맨 뒤에 추가
# # print(fruits)
# #
# # fruits.extend(['kiwi', 'melon']) # 리스트의 요소를 꺼내서 추가
# # print(fruits)
# #
# # fruits.insert(1, 'mango') # 인덱스에 요소 추가 뒤로 하나 씩 밀림
# # print(fruits)
# #
# # fruits.remove('banana') # 요소 제거
# # print(fruits)
# #
# # removed = fruits.pop(1) # 인덱스의 요소를 제거하고 제거된 요소를 반환
# # print(fruits, removed)
# #
# # print(fruits.index('orange')) #요소의 인덱스
# # # print(fruits.index('water')) #없는 요소의 인덱스 ValueError
#
# numbers = [1,2,2,3,2,4,]
# print(numbers.count(2))  # 2라는 요소의 개수
#
# # list.sort() : 리스트 자체를 정렬함, 정렬한 후에 원래 리스트는 알 수 없음
# # sorted() 함수 : 원본 리스트 보존하고 새로 정렬된 리스트를 만듬
# scores = [75, 90 ,65, 100, 85]
# scores.sort() # 오름차순 정렬, (ascending sort)
# print(scores)
# scores.sort(reverse=True) # 내림차순 정렬 (desending sort)
# print(scores)
#
# scores.reverse() # 요소의 순서를 180 도뒤집음
# print(scores)
#
# # 깊은 복사 (deep copy) : 똑같은 메모리를 복사 , 메모리에 원본이 2개, 변수 2개
# # 얕은 복사 (shallow copy) : 참조를 복사, 메모리에 원본이 1개, 변수 2개
# scores_copy = scores.copy() # 리스트 복사 (앝은 복사)
# print(f'원본리스트 : {scores}')
# print(f'복사 리스트 : {scores_copy}')
#
# temp = [1,2,3]
# temp.clear() # 모든 요소 제거
# print(temp) # empty list : 요소가 없는 리스트
#
# # 2. dictionary 주요 메소드
#
# students = {
#     'name' : '홍길동',
#     'age' : 25,
#     'score' : 90,
# }
# print(students)
#
# print(students.keys())
# print(type(students.keys())) # <class 'dict_keys'>
# print(list(students.keys())) # ['name', 'age', 'score']
#
# print(students.values()) # 값 추출
# print(type(students.values()))  # <class 'dict_values'>
# print(list(students.values())) #['홍길동', 25, 90]
#
# print(students.items()) # 아이템 추출
# print(type(students.items())) # <class 'dict_items'>
# print(list(students.items())) #[('name', '홍길동'), ('age', 25), ('score', 90)]
#
# print(students.get('name')) # 키에 매핑된 값
# print(students.get('address')) # None 없는 키를 찾으면
# print(students.get('hoby', '축구')) # 키가 없으면 뒤의 기본값 획득
#
# # 키가 있으면 값을 수정, 키가 없으면 아이템을 생성해 추가
# students.update({
#     'score' : 95, # 값을 수정
#     'grade' : 'A'   # 아이템 생성
# })
# print(students)
#
# students.setdefault('city', '서울') # 키가 없으면 기본값을 추가
# print(students)
# students.setdefault('score', 0) # 키가 있으면 값 변동 없음
# print(students)
#
# removed_value = students.pop('age') # 키에 해당한 item 을 제거 하고  값을 반환
# print(students)
# print(removed_value)
#
# last_item = students.popitem() # 마지막 아이템을 제거하고 튜플로 반환
# print(students,last_item)
#
# students_copy = students.copy() # 얕은 복사
# print(students,students_copy)
#
# temp_dict = {'a' : 1, 'b' : 2}
# temp_dict.clear() # 모든 아이템 제거
# print(temp_dict) # 아이템 없는 딕셔넌리 (empty dictionary)


# # 3. set 주요 메소드
numbers = {1, 2, 3, 4}
print(numbers)

numbers.add(5) # 요소 추가
print(numbers)

numbers.update([6,7,8])
print(numbers)

numbers.remove(3) # 요소삭제
print(numbers)

numbers.discard(100) # 요소가 있으면 삭제, 없어도 에러 없음

removes_value = numbers.pop() #임의의 요소를 삭제하고 삭제된 요소 반환
print(numbers, removes_value)

numbers_copy = numbers.copy()
print(numbers, numbers_copy)

temp_set = {1,2,3}
temp_set.clear() # 모든 요소 제거
print(temp_set) # set() : 요소가 없는 셋 (empty set)

python_students = {'철수', ' 영희', '민수', '지수'}
ai_students = {'영희', '민수', '준호'}

print(f'합집합 : {python_students.union(ai_students)}')
print(f'합집합 : {python_students | ai_students}')

print(f'교집합 : {python_students.intersection(ai_students)}')
print(f'합집합 : {python_students & ai_students}')


print(f'차집합 : {python_students.difference(ai_students)}')
print(f'차집합 : {python_students - ai_students}')

#둘중 하나만 수강
print(f'매칭차집함 : {python_students.symmetric_difference(ai_students)}')
print(f'매칭차집함 : {python_students ^ ai_students}')

a = {1,2}
b = {1,2,3,4}
c = {5,6}

print(a.issubset(b)) # a가 b의 부분집합인지
print(b.issuperset(a)) # b가 a의 상위 집합인지

# 문자열과 리스트 슬라이싱
str = 'Hello There'
print(str[0]) # index 0 문자
print(str[:3]) # Hel index 0 ~ 2
print(str[3:]) # lo There index 3 ~~
print(str[3:5]) # lo, index 3 4
print(str[::2]) # HloTee index 0 ~~  step 2 문자열

even = [2,4,6,8]
odd = [1,3,5,7]
print(even[0]) # 2
print(odd[2: ]) # [6, 8] index 2 ~~
print(even[:3]) #[2,4,6] index 0 ~ 2
print(even[1:4]) # [4,6,8] index 1~3
print(even[::2]) # [2,6] index 0 ~~ step 2
print(even[-1]) # 8 index 맨 디에서 첫 번쨰

# 문자열, 리스트 병합 / 반복

str1 = 'Hellow'
str2 = ' PyThon'
print(str1 + str2)  # 병합
print(str * 3) # 3번 반복

list1 = [1,2]
list2 = [3,4,5]
print(list1 + list2) #병합
print(list1 * 3) # 3번 반복















