# day8_challenge.py
# [AI휴먼 Day 8 Challenge 과제]
# 주제: 클래스 기반 학생 성적 관리 미니 프로그램
#
# 목표
# 클래스, 리스트, 반복문, 조건문, 함수, 파일 처리를 통합할 수 있습니다.
# 여러 Student 객체 중 조건에 맞는 객체를 필터링할 수 있습니다.
#
# 요구사항
# Student 클래스를 작성하십시오.
# name, score 속성을 저장하십시오.
# grade() 메서드를 작성하십시오.
# 80점 이상: PASS
# 그 외: RETRY
# show() 메서드를 작성하십시오.
# 아래 5명의 Student 객체를 생성하고 리스트에 저장하십시오.
# 김민수 85
# 이서연 92
# 박지훈 76
# 정하늘 88
# 오세진 69
# 전체 학생 정보를 출력하십시오.
# PASS 학생만 골라서 출력하십시오.
# 전체 평균 점수를 계산해 소수점 첫째 자리까지 출력하십시오.
# PASS 학생 수를 출력하십시오.
# 결과를 day8_challenge_result.txt 파일에 저장하십시오.
#  파일에는 각 학생의 이름, 점수, 결과가 한 줄씩 들어가야 합니다.
#  마지막 줄에는 평균 점수와 PASS 학생 수를 기록하십시오.
# 파일 저장 부분은 try-except로 감싸십시오.



class Student:#
    def __init__(self,name,score):
        self.name = name
        self.score = score

    def grade(self): # 통과인지 아닌지
        if self.score >= 80:
            return 'PASS'
        else:
            return 'RETRY'

    def show(self):# 츨력
        print(f'{self.name},{self.score},{self.grade()}')
# 리스트 생성
students=[]
student1 = Student('김민수',85)
student2 = Student('이서연',92)
student3 = Student('박지훈',76)
student4 = Student('정하늘',88)
student5 = Student('오세진',69)

students=[student1,student2,student3,student4,student5]

#전체 학생 출력
def all_show(students):
    print('\n[전체학생]')
    for student in students:
        student.show()
#전체 평균
def avg_student(students):
    avg = 0
    for student in students:
        avg += student.score
    average = avg/len(students)
    return f'전체 평균{average:.1f}\n'
#합격자수
def is_pass_count(students):
    pass_count = 0
    for student in students:
        if student.score >= 80:
            pass_count += 1
    return f'PASS 학생수 :{pass_count}'

# 합격 학생만 출력
def is_pass_students(students):
    print('\n[합격 학생]')
    for student in students:
        if student.grade() == 'PASS':
            student.show()

all_show(students)
is_pass_students(students) # 합격 학생 출력
print(avg_student(students)) # 학생 전체 평균 출력
print(is_pass_count(students)) # 통과 학생수 출력

# 경로생성
DATA_DIR = 'day_challenge_result.txt'
# 텍스트 파일 생성 후 작성
try:
    with open(DATA_DIR,'w',encoding='utf-8',newline='') as f:
        f.write('[합격 학생]\n')
        for student in students:
            if student.grade() == 'PASS':
                f.write(f'{student.name},{student.score},{student.grade()}\n')
        f.write(avg_student(students))
        f.write(is_pass_count(students))
except FileNotFoundError:
    print('파일이 없습니다')
# 예시 출력 일부
# [합격 학생]
# 김민수 85 PASS
# 이서연 92 PASS
# 정하늘 88 PASS
# 전체 평균: 82.0
# PASS 학생 수: 3

# 확인 포인트
# 객체 리스트를 반복문으로 처리하는가?
# 합격 여부 판단을 grade() 메서드에 모았는가?
# 평균과 합격자 수를 정확히 계산하는가?
# 파일 저장 중 오류를 처리하는가?