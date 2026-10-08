# # day8_application.py
# [AI휴먼 Day 8 Application 과제]
# 주제: 메서드를 가진 Student 클래스 만들기
#
# 목표
# 객체의 속성을 메서드에서 활용할 수 있습니다.
# 조건문을 메서드 내부에 적용할 수 있습니다.
# 여러 객체를 리스트에 저장해 반복 처리할 수 있습니다.

# 요구사항
# Student 클래스를 작성하십시오.
# name과 score를 속성으로 저장하십시오.
# grade() 메서드를 작성하십시오.
# 80점 이상이면 "PASS"
# 80점 미만이면 "RETRY"
# show() 메서드를 작성하십시오.
# 이름, 점수, grade() 결과를 한 줄에 출력하십시오.
# 다음 학생 4명의 객체를 생성하십시오.
# 김민수 85
# 이서연 92
# 박지훈 76
# 정하늘 88
# 객체들을 students 리스트에 저장하십시오.
# for 반복문으로 모든 학생의 show() 메서드를 호출하십시오.


class Student:
    def __init__(self,name,score):
        self.name = name
        self.score = score

    def grade(self):
        if self.score >=80:
            return 'PASS'
        else:
            return 'RETRY'

    def show(self):
        print(f'이름:{self.name},점수:{self.score},결과:{self.grade()}')




student1 = Student('김민수',85)
student2 = Student('이서연',92)
student3 = Student('박지훈',76)
student4 = Student('정하늘',88)
students=[student1,student2,student3,student4]

for student in students:
    student.show()

# 예시 출력
# 이름: 김민수, 점수: 85, 결과: PASS
# 이름: 이서연, 점수: 92, 결과: PASS
# 이름: 박지훈, 점수: 76, 결과: RETRY
# 이름: 정하늘, 점수: 88, 결과: PASS
#
# 확인 포인트
# grade()가 값을 return 하는가?
# show()에서 self.grade()를 호출하는가?
# 리스트와 for 반복문으로 객체들을 처리하는가?
