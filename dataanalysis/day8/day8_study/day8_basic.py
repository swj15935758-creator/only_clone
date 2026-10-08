# day8_basic
# [AI휴먼 Day 8 Basic 과제]
# 주제: Student 클래스와 객체 생성
#
# 목표
# 클래스를 직접 정의할 수 있습니다.
# init()과 self를 사용할 수 있습니다.
# 같은 클래스로 여러 객체를 만들 수 있습니다.
#
# 요구사항
# Student 클래스를 작성하십시오.
# init(self, name, score)를 작성하십시오.
# 전달받은 name과 score를 각각 self.name, self.score에 저장하십시오.
# 아래 두 학생 객체를 생성하십시오.
# 김민수, 85점
# 이서연, 92점
# 각 객체의 name과 score 속성을 직접 출력하십시오.
# 출력 형식은 다음과 비슷하게 작성하십시오.
# 김민수 85
# 이서연 92

class Student:
    def __init__(self,name,score):
        self.name = name
        self.score = score

student1 = Student('김민수',85)
student2 = Student('이서연',92)

def show_student(self):
    print(f'{self.name},{self.score}')

show_student(student1)
show_student(student2)

# class Student:
#     def __init__(self, name, score):
#         self.name = name
#         self.score = score
#
# student1 = Student('김민수', 85)
# student2 = Student('이서연', 92)
#
# print(student1.name, student1.score)
# print(student2.name, student2.score)
# 제약사항
# 딕셔너리 대신 Student 클래스를 사용하십시오.
# 아직 show() 메서드는 만들지 않아도 됩니다.

# 확인 포인트
# class 키워드를 올바르게 사용했는가?
# init()에 self가 있는가?
# 두 객체가 서로 다른 값을 가지는가?
