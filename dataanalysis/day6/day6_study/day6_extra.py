# [AI휴먼 6일차 추가 실습]
# 주제: Python 함수 실습
# 문항 수: 10문항
#
# ============================================================
# 1. 리스트에서 최댓값과 최솟값 찾기
# ============================================================
#
# 숫자 리스트를 매개변수로 전달받아 최댓값과 최솟값을 각각 구한 뒤
# 두 값을 튜플 형태로 반환하는 find_min_max() 함수를 작성하세요.
#
# 단, max(), min() 내장 함수는 사용하지 마세요.
#
# [실행 예]

def find_min_max(nums):
    min_val=0
    max_val=0
    for num in nums:
        if num < min_val:
            min_val = num
    for num in nums:
        if num > max_val:
            max_val = num
    return min_val, max_val


numbers = [17, 5, 23, 9, 11]
result = find_min_max(numbers)
print(result)
#
# [출력 예]
# (5, 23)
#
#
# ============================================================
# 2. 합격자 점수만 추출하는 함수
# ============================================================
#
# 학생 점수 리스트를 전달받아 60점 이상인 점수만 새로운 리스트에
# 저장하여 반환하는 get_pass_scores() 함수를 작성하세요.
#
# 단, filter() 함수와 리스트 컴프리헨션은 사용하지 마세요.
#
# [실행 예]


def get_pass_scores(scs):
    pass_score = []
    for score in scs:
        if score >= 60:
            pass_score.append(score)
    return pass_score


scores = [45, 72, 88, 59, 60, 91]
print(get_pass_scores(scores))
#
# [출력 예]
# [72, 88, 60, 91]
#
#
# ============================================================
# 3. 문자열 분석 결과 반환 함수
# ============================================================
#
# 문자열 하나를 전달받아 다음 정보를 계산하는 analyze_text() 함수를 작성하세요.
#
# 1) 전체 문자 수
# 2) 공백을 제외한 문자 수
# 3) 문자열에 포함된 숫자 문자의 개수
#
# 계산 결과는 다음 형식의 딕셔너리로 반환하세요.
#
# {
#     "전체문자수": 값,
#     "공백제외문자수": 값,
#     "숫자개수": 값
# }
def analyze_text(text):

    # 1) 총문자수
    total_chars = len(text)
    # 2) 공백을 제외한 문자 수 계산
    total_empty = 0
    for char in text:
        if char == " ":
            total_empty += 1

    no_spaces = total_chars - total_empty

    # 3) 숫자 문자의 개수 계산 (비교 연산자 활용)
    digit_count = 0
    for char in text:
        # 글자가 '0'에서 '9' 사이의 문자인지 직접 비교합니다.
        if "0" <= char <= "9":
            digit_count += 1

    # 결과 딕셔너리 반환
    return {
        "전체문자수": total_chars,
        "공백제외문자수": no_spaces,
        "숫자개수": digit_count
    }


# 실행 예시
text = "Python 3 Function 2026"
print(analyze_text(text))
# 출력: {'전체문자수': 22, '공백제외문자수': 19, '숫자개수': 5}


#
# [출력 예]
# {'전체문자수': 22, '공백제외문자수': 19, '숫자개수': 5}
#
#
# ============================================================
# 4. 학생별 총점과 평균 계산 함수
# ============================================================
#
# 다음과 같은 학생별 점수 딕셔너리가 있습니다.
#
students = {
    "김철수": [80, 90, 70],
    "이영희": [95, 88, 92],
    "박민수": [60, 75, 68]
}

def avg_student(students_list):
    total = 0
    for scores in students_list:
        total += scores
    average = total / len(students_list)
    return average

def sum_student(students_list):
    total = 0
    for scores in students_list:
        total += scores
    return total

def calculate_student(student):
    for name,scores in student.items():
        average=avg_student(scores)
        total = sum_student(scores)
        print({"이름": name, "총점": total, "평균": average})

print(calculate_student(students))
# 학생 이름과 점수 리스트를 전달받아 총점과 평균을 계산하여
# 딕셔너리로 반환하는 calculate_student() 함수를 작성하세요.
#
# 반환 형식은 다음과 같습니다.
#
# {
#     "이름": 학생이름,
#     "총점": 총점,
#     "평균": 평균
# }
#
# 그리고 반복문을 이용하여 모든 학생의 결과를 출력하세요.
#
# [출력 예]
# {'이름': '김철수', '총점': 240, '평균': 80.0}
# {'이름': '이영희', '총점': 275, '평균': 91.66666666666667}
# {'이름': '박민수', '총점': 203, '평균': 67.66666666666667}
#
#
# ============================================================
# 5. 가변 인수를 이용한 합계 함수 *argus
# ============================================================
#
# 전달되는 숫자의 개수가 정해져 있지 않을 때 사용할 수 있도록
# 가변 인수 *args를 이용하여 모든 숫자의 합을 반환하는
# sum_all() 함수를 작성하세요.
#
# 파이썬의 내장 함수 sum()은 사용하지 마세요.
#
# [실행 예]

def sum_all(*args):
    total = 0

    for num in args:
        total += num

    return total


print(sum_all(10, 20, 30))
print(sum_all(1, 2, 3, 4, 5))

#
# [출력 예]
# 60
# 15
#
#
# ============================================================
# 6. 기본값 매개변수를 이용한 급여 계산 함수
# ============================================================
#
# 기본 급여와 보너스율을 전달받아 최종 급여를 계산하는
# calculate_salary() 함수를 작성하세요.
#
# 최종 급여 = 기본 급여 + (기본 급여 × 보너스율)
#
# 보너스율의 기본값은 0.1(10%)로 설정하세요.

def input_salary(a):
    salary = a
    return salary


def input_bonous(b):
    bonus =b
    return bonus


def result_salary(a, b):
    salary = input_salary(a)
    bonus = input_bonous(b)
    result = salary + (salary * bonus)
    return result


def calculate_salary(a, b=0.1):
    return result_salary(a, b)


# [실행 예]
print(calculate_salary(3000000))
print(calculate_salary(3000000, 0.2))


# [출력 예]
# 3300000.0
# 3600000.0
#
#
# ============================================================
# 7. 함수를 이용한 학생 성적 처리
# ============================================================
#
# 아래와 같은 학생 점수 딕셔너리가 있습니다.
#
students = {
    "김철수": 85,
    "이영희": 92,
    "박민수": 76,
    "최지우": 64
}
#
# 다음 2개의 함수를 작성하세요.
#
# 1) get_grade(score)
#    - 점수를 전달받아 A, B, C, D, F 중 하나를 반환

def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"



# 2) make_report(students)
#    - 학생 딕셔너리를 전달받아
#      "이름 : 점수점 / 등급"
#      형식의 문자열 리스트를 반환

#내코드
# def make_report(students):
#
#     for name,scores in students.items():
#         grade = get_grade(scores)
#         print(f'{name}: {scores}점/{grade}')

#강사님 코드
def make_report(students):
    report = [] # 결과 저장 리스트
    for name, score in students.items():
        grade = get_grade(score)
        line = f'{name}:{score}점/{grade}'
        report.append(line) # 한줄 저장
    return report

result = make_report(students)

for line in result:
    print(line)

# [출력 예]
# 김철수 : 85점 / B
# 이영희 : 92점 / A
# 박민수 : 76점 / C
# 최지우 : 64점 / D
#
#
# ============================================================
# 8. 고차함수 - 계산 함수를 인수로 전달하기
# ============================================================
#
# 함수를 다른 함수의 인수로 전달하는 고차함수를 작성하세요.
#
# 다음 함수들을 작성하세요.
#
# 1) add(a, b)      : 두 수의 합 반환
# 2) subtract(a, b) : 두 수의 차 반환
# 3) multiply(a, b) : 두 수의 곱 반환
# 4) calculate(a, b, operation)
#    - a, b와 함께 계산 함수를 operation으로 전달받아
#      해당 함수의 실행 결과를 반환

def add(a,b):
    return a+b

def subtract(a,b):
    return a-b
def multiply(a,b):
    return a*b
def divide(a,b):
    return a/b

# 고차함수 : 두인수와 콜백함수를 파라미터로
def calculate(a,b, operation):
    return operation(a,b) # 콜백 함수에 두인수를 전달해 처리

# [실행 예]
print(calculate(10, 5, add))
print(calculate(10, 5, subtract))
print(calculate(10, 5, multiply))

# [출력 예]
# 15
# 5
# 50
#
#
# ============================================================
# 9. 콜백함수 - 주문 처리 완료 후 함수 호출하기
# ============================================================
#
# 온라인 주문 처리 상황을 함수로 구현하세요.
#
# 다음 함수를 작성하세요.
#
# 1) payment_complete(order_name)
#    - "[주문명] 결제가 완료되었습니다." 출력
def payment_complete(order_name):
    print(f'{order_name} 결제 완료')

# 2) send_message(order_name)
#    - "[주문명] 주문 완료 메시지를 전송했습니다." 출력
def send_message(order_name):
    print(f'{order_name} 주문완료 메세지 전송')

# 3) process_order(order_name, callback)
#    - "[주문명] 주문을 처리합니다." 출력
#    - 처리가 끝난 후 callback(order_name)을 호출
def process_order(order_name, callback):
     print(f'{order_name} 주문처리')
     return callback(order_name)


# process_order()에 서로 다른 콜백함수를 전달하여
# 다른 후속 작업이 실행되는 것을 확인하세요.
#
# [실행 예]
process_order("노트북", payment_complete)
process_order("키보드", send_message)
#
# [출력 예]
# [노트북] 주문을 처리합니다.
# [노트북] 결제가 완료되었습니다.
# [키보드] 주문을 처리합니다.
# [키보드] 주문 완료 메시지를 전송했습니다.
#
#
# ============================================================
# 10. 고차함수 + 콜백함수 - 점수 데이터 처리 시스템
# ============================================================
#
# 학생 점수 리스트를 다양한 기준으로 처리할 수 있는 프로그램을 작성하세요.
#
scores = [55, 72, 88, 91, 67, 100, 83]

# 1) is_pass(score)
def is_pass(score):
    return score >= 60

# 2) is_excellent(score)
def is_excellent(score):
    return score >= 90

# 3) filter_scores(scores, condition)
def filter_scores(scores, condition):
    result = []
    for score in scores:
        if condition(score): 
            result.append(score)
    return result

# 4) print_result(title, result)
def print_result(title, result):
    print(f'{title} : {result}')

# 5) process_scores(scores, condition, callback, title='결과')
def process_scores(scores, condition, callback, title='결과'):
    filtered_scores = filter_scores(scores, condition)
    callback(title, filtered_scores)
    return filtered_scores

# [실행 예]
process_scores(scores, is_pass, print_result)
process_scores(scores, is_excellent, print_result)

#
# [출력 예]
# 결과 : [72, 88, 91, 67, 100, 83]
# 결과 : [91, 100]