# day8_ex1.py
# 클래스, 객체, 인스턴스, 속성(인스턴스), 기능(메서드), 생성자

#클래스 정의 = 사용자 정의타입(User Defind Type) 생성
class Student:
    # 생성자 (constructor)
    # 역할 : 객체가 가지는 인스턴스 변수의 값을 초기화
    # self.name, self.score : 인스턴스 변수
    # name, score : 생성자 파라미터
    def __init__(self, name, score):
        self.name = name
        self.score = score

    # 메소드(method) : 객체로 접근하는 함수
    def grade(self): # 합격인지 재시도인지 문자열 출력
        if self.score >= 80:
            return 'PASS'
        else:
            return 'RETRY'


    def show(self): # 이름 점수 결과를 출력해주는 메소드
        print(f'이름: {self.name}, 점수 :{self.score}, 결과ㅣ:{self.grade()}')

# 객체 리스트를 받아서 리스트 내의 객체들의 정보를 출력하는 함수
def show_all_students(students):
    print('\n[전체학생]')
    for student in students: # 학생 수만큼 반복
        student.show()

# 객체 리스트를 받아서 합격한 학생들의 정보를 출력하는 함수
def show_pass_students(students):
    print('\n[합격 학생]')
    for student in students:
        if student.grade() == 'PASS':
            student.show()

# 전체 학생들의 점수의 평균을 반환화는 함수
def get_average(students):
    total = 0 # 총점
    for student in students:
        total += student.score
    return total / len(students)

# 학생 리스트와 파일명을 전달 받아 출력하고 레포트로 저장
def save_report(students, filename):
    try:
        with open(filename,'w',encoding='utf-8') as f:
            f.write('[학생 성적 결과]\n')
            for student in students:
                line = f'{student.name},{student.score},{student.grade()}\n'
                f.write(line)
            f.write(f'평균,{get_average(students):.1f}\n')
        print(f'\n결과가 {filename} 파일에 저장되었습니다.')
    except FileNotFoundError:
        print(f'파일을 찾을 수 없습니다!')

# main 실행 함수
def main():

    # 객체 4개 생성
    student1 = Student('감민수',85)
    student2 = Student('이서현',92)
    student3 = Student('박지훈',76)
    student4 = Student('정하늘',88)

    # 리스트에 객체 4개로 된 리스트 생성
    students = [student1, student2, student3, student4]

    show_all_students(students) # 모든 학생 정보 출력
    show_all_students(students) # 합격 학생 정보 출력
    average = get_average(students) # 평균

    print(f'\n전체 평균 : {average:.1f}')

    save_report(students, 'dat8_result.txt')

# 현재 파일이 메인 모듈이면 main()함수로 실행
# __name__ : 현재 모듈명
# → 파이썬이 자동으로 만들어주는 특별한 변수
# → 현재 모듈이 어떤 이름으로 실행되고 있는지 저
if __name__ =='__main__':
    main()


'''
[객체 지향 프로그램의 개념 정리]
1. 객체지향의 4대 개념

    1) 상속(inheritance)
        - 기존에 만들어 놓은 클래스를 재사용(reusing)
        - 기존에 만들어 놓은 클래스의 변수와 메소드를 상속받아 확장(extension)
        - 상속 해주는 클래스 : 상위(super), 기반(base), 부모(parent) 클래스라 부름
        - 상속을 받는 클래스 : 하위(sub), 파생(derived), 자식(child)클래스라 부름
        
    2) 다형성 (polymophism)
        - 같은 형태인데 다른 기능 구현
        - 메소드 오버라이딩(method overriding)
        - 상위 클래스의 메소드와 동일한 메소드를 하위 클래스에 정의하고
          다른 구현을 하도록 함
        - 상위에는 추상적인것, 하위에는 구체적인것
    
    3) 추상화 (Abstraction)
        - 현실셰게의 복잡하고 다양한 사물이나 개념을 최대한 단순화 시킴
          단, 본연의 성질을 잃어버리지 않는 선에서 단순화 시켜야 함
        - 클래스를 정의한다는 건 어떤 사물이나 개념을 추상화 시키는 것
    
4) 캡슐화 (Encapsulation) = 정보 은닉(Information Hiding)
    - 클래스 내부의 데이터 (객체의 데이터)에 대한 접근과 변경을 외부로부터 보호

2. 클래스 변수와 인스턴스 변수
    1) 클래스 변수
        - 클래스 내부, 생성자 외부에 만드는 변수
        - 클래스 변수는 메모리에 하나만 생성됨
        - 클래스 변수는 모든 객체가 값을 공유
    
    2) 인스턴스 변수(=객체변수)
        - 생성자 내부에 self.변수명 형태로 만드는 변수
        - 인스턴스 변수는 객체마다 따로 가짐
   
    
'''
