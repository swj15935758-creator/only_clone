# day4/day4_ex.py
# 조건식, bool, if, elif, else, 논리연산자, 중첩 조건

# # 1. bool 비교연산자
# score = 85
# print(score >= 80)
# print(score <  60)
# print(score == 85)
# print(score != 85)

# # 2. if
# temperature = 31
# if temperature >= 30:
#     print('폭염 주의')
# print('기온 확인 완료')

# # 3. if ~ else
# score = 75
# if score >= 80:
#     print('Pass')
# else:
#     print('RETRY')

# # 4. if ~ elif ~ else
# score = 85
# if score >= 90: # 90이상
#     grade = 'A'
# elif score >= 80: # 80이상 90미만
#     grade = 'B'
# elif score >= 70: #70이상 80미만
#     grade = 'C'
# elif score >= 60: #60이상 70 미만
#     grade = 'D'
# else:             # 60미만
#     grade = 'F'
# print(f'점수 :{score}, 등급 : {grade}')

# # 5. 논리연산자 and
# score = 82  # 점수
# attendance = 91 #참여자수
# if score >= 70 and attendance >= 80:
#     print('PASS')
# else:   # 두 조건중 하나라도 FALSE
#     print('FAIL')

# # 6. 논리 연산자 or
# score = 95      #시험점수
# project_score = 72  #프로젝트 점수
# if score >= 90 or project_score >= 90:
#     print('우수한 항목이 있습니다.')
# else:   #두조건 모두 False
#     print('우수한 항목이 없습니다.')

# # 7. 논리 연산자 not
# is_login = False # 로그인 여부
# if not is_login:
#     print('로그인이 필요합니다')
# else:
#     print('서비스 이용이 가능합니다')

# # 8. 중첩 조건문
# score = 85
# attendance = 75
# if score >= 70: #점수가 70이상
#     if attendance >= 80: # 점수가 70 이상이고 출석률이 80 이상
#         print('PASS')
#     else: #  점수는 70 이상인데 출석률이 80 미만
#         print('FAIL: 출석률 부족')
# else: # 점수가 70미만
#     print('FAIL: 점수가 부족하다')

# # 9. 입력값, 조건문
# # **범위 체크부터한다**
# user_score = int(input('점수를 입력하세요(0~100): '))
# if user_score <0 or user_score > 100: # 범위가 벗어남
#     print('입력 오류 : 점수는 0~100 사이여야 합니다')
# elif user_score >= 60: #정상 범위 이고
#     print('PASS')
# else: # 정상 범위이고 점수 60미만
#     print('RETRY')

# 10. 조건 기반 성적 판정
score = int(input('성적(0~100): '))
attendance = int(input('출석률(0~100): '))

if score < 0 or score > 100: # 성적에 대한 범위 체크
    print('입력 오류: 성적은 0~100 사이여야 합니다')
elif attendance < 0 or attendance > 100:
    print('입력 오류: 출석률은 0 ~ 100 사이여야 합니다')
else:#입력 값들이 범위 내에 있다
    if score >= 90:
        grade = 'A'
    elif score >= 80:
        grade = 'B'
    elif score >= 70:
        grade = 'C'
    elif score >= 60:
        grade = 'D'
    else:
        grade = 'F'
    if score >= 90 and attendance >= 90:
        result = '우수 합격' # 결과
        reason = '점수와 출석률이 모두 우수' # 판정사유
    elif score >= 70 and attendance >= 80:
        result = '합격'
        reason = '점수와 출석률 기준 충족'
    elif attendance < 80: #출석률이 부족
        result = '불합격'
        reason = '출석률 부족'
    else: # 점수가 부족
        result = '불합격'
        reason = '점수가 부족'
    print(f'등급: {grade} \n'
          f'합격여부 : {result} \n'
          f'사유 : {reason}')

     




















