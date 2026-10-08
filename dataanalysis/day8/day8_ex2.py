# day8_ex2.py
# 클래스 변수, 인스턴스 변수

class Student:
    school = 'AI휴먼 고등학교' # 클래스 변수
    def __init__(self,name): #생성자 new*
        self.name = name # self.name : 인스턴스 변수, name: 생성자 파라미터

#객체 2개 생성
hong = Student('홍길동')
kang = Student('강감찬')

# 객체 정보를 출력 함수
def show_info(student):
    print(f'{student.name}님은 {Student.school}에 다닙니다.')



# 인스턴스 변수 값 변경
# 인스턴수 변수 값 변경은 다른 객체의 인스턴스 값에
# 영향을 주지 않음= 객체마다 인스턴스변수를 따로 가짐
hong.name = '홍말똥'
show_info(hong) # 홍말똥
show_info(kang) # 강감찬

# 클래스 변수 값 변경
# 클래스 변수의 값 변경은 모든 객체에 영향을 미침 **메모리에 하나밖에 없기 떄문**
Student.schoo = 'AI퀀트 고등학교'
show_info(hong)
show_info(kang)

# 결론
# 모든 객체가 공유해야 하는 값은 크래스 변수에 저장
# 객체마다 각각 가져야 하는 값은 인스턴스 변수에 저장


