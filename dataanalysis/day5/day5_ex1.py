# day5_ex1.py
# 반복문 (for, while), 컬랙션(List, Turple, Dictionary, Set)

# # 1. for 문으로 순차적 값 출력
# scores = [72, 88, 95, 61] # len: 4 index range: 0 ~ 3
# for score in scores:
#     print(score, end=' ')
#
# greeting =  'Hello python'
# print(greeting)
# for letter in greeting:
#     print(letter, end=' ')

# # 2. for문 + 조건문
# scores = [72, 88, 95, 61]  # len: 4 index range: 0 ~ 3
# for score in scores:
#     if score >= 80:
#         print(score, "PASS")
#     else:
#         print(score, "RETRY")
# print()

# # 3. range()
#
# for i in range(5): # 0~4
#     print(i, end=" ")
# print()
#
# for i in range(1, 10): # 1 ~ 9
#     print(i, end=" ")
# print()
#
# for i in range(1, 20, 2):
#     print(i, end=" ")
# print()

# # 4. while
# count = 1
# while count <= 5:
#     print(count, end=" ")
#     count += 1 # while 종료 조건
# print()

# # 5. 리스트 함계 계산
# scores = [72, 88, 95, 61]  # len: 4 index range: 0 ~ 3
# total = 0 # 합계 저장 변수
# for score in scores:
#     total += score
# print(f'합 계 :{total}')
# print(sum(scores)) # sum() 함수 사용
# print(f'평균 :{total / len(scores)}') #len 함수 사용 scores 의 길이 4fmf s>

# # 6. 합격자 수 계산
# scores = [72, 88, 95, 61]  # len: 4 index range: 0 ~ 3
# pass_count = 0 # 합격자수 변수
# for score in scores:
#     if score >= 80:
#         pass_count += 1 #조건을 만족하면 1증가
# print(f'합격자 수 :{pass_count}')

# # 7. 최고점 계산
# scores = [72, 88, 95, 61]  # len: 4 index range: 0 ~ 3
# highest = scores[0]
# for score in scores:
#     if score > highest:
#         highest = score
# print(f'최고점 : {highest}')
# print(max(scores)) # 최대값
# print(min(scores)) # 최솟값

# # 8. Dictionary에 이름과 점수를 저장
# student = { # item 이 4개인 딕셔너리
#     '민수' : 72,
#     '지연' : 88,
#     '준호' : 95,
#     '서연' : 61,
# }
# for name, score in student.items(): #아이템 수만큼 반복 개수가 늘어남에 따라 for 과 in 사이가 길어짐
#     print(f'이름:{name} 점수: {score}')

# # 9. 학생별 등급 판정
# student = { # item 이 4개인 딕셔너리
#     '민수' : 72,
#     '지연' : 88,
#     '준호' : 95,
#     '서연' : 61,
# }
# for name, score in student.items():
#     if score >= 90:
#         grade = "A"
#     elif score >= 80:
#         grade = "B"
#     elif score >= 70:
#         grade = "C"
#     elif score >= 60:
#         grade = "D"
#     else:
#         grade = "F"
#     print(f'이름: {name}, 점수 : {score}, 등급: {grade}')

# # 10. 중첩 for 문
# for i in range(2, 10): # 2~9 각단 outer for , 행의 의미
#     for j in range(1, 10): #1 ~9 곱해지는수  inner for , 열의 의미
#         print(f'{i} x {j} = {i * j}', end='')
#         print() #줄 바꿈
#     print() # 줄바꿈 + 단 구분

# # break : 반복문 내에 사용하고 가장 가까운 반복문 을 즉시 빠져 나감
# for i in range(2, 10):
#     for j in range(1, 10):
#         if i % 2 == 0: # i 가 짝수라면
#             break  # inner for 문을 벗어남
#         print(f'{i} x {j} = {i * j}', end='')
#         print()
#     print()
#
# # continue : 반복문 내에서 continue를 만나면 하단 코드를 수행 x 다음번 반복 수행
# for i in range(1,11):# 1 ~10
#     if i % 2 == 0: # i가 짝수 면
#         continue # 하단 코드 출력  x 다음 반복을 수행
#     print(i, end=' ')
# print()
#
#
# # enumerate(이터러블, 시작번호) 함수 : 요소 반복시 순서 번호 부여
# scores = [95, 88 ,76, 100]
# for i, score in enumerate(scores, start=1):
#     print(f'{i}번 요소 : {score}')
#
# # zip(이터러블, 이터러블 ...) 함수 : 여러 이터러블 동시 묶어서 반복
# names =['홍길등','김강찬','이순신']
# ages = [20, 30, 40]
# jobs =['산적','장군','장군']
#
# for name,job , age in zip(names,jobs,ages):
#     print(f'이름: {name}  직업은 {job} 나이는 {age}입니다')

# # emerate ,zio 동시
# names =['홍길등','김강찬','이순신']
# scores = [20, 30, 40]
# for i,(name,score) in enumerate(zip(names,scores),start=1):
#     print(f'[{i}번]  이름 : {name}, 성적 :  {score}')





