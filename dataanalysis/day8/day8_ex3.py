# day8_ex3.py
# 상속, 오버라이딩

# 상위 클래스 : 추상적, 설계의 개념, 공통의 개념
class Animal:
    def __init__(self, name):
        self.name = name
    def sound(self):
        print('동물소리???')



# 하위클래스 : 구체적, 구현의 개념, 개별의 개념
# Animal 을 상속 받은 하위 클래스
# Animal 에 있는 name과 sound를 정의하지 않아도 사용가능
class Dog(Animal):
    type = '강아지'
    # 메소드 오버라이딩 : 상위클래스의 메소드를 재구현해서 다른 기능을 정의
    def sound(self):
        print(f'{self.name}은 {Dog.type} "깽깽" 소리를 냅니다.')


class Cat(Animal):
    type = '고양이'
    # 메소드 오버라이딩 : 상위클래스의 메소드를 재구현해서 다른 기능을 정의
    def sound(self):
        print(f'{self.name}은 {Cat.type} "미야옹" 소리를 냅니다.')

animals = [
    Dog('브라운'),
    Cat('엘리자베스'),
    Dog('행성 파괴자'),
    Cat('엘리자베스 동생 콘트라베이스')
]

# 오버라이딩의 목적이자 존재 이유
# 다른 타입일지라도 Animal을 상속 받은 타입은
# sound메소드로 각자의 소리를 낼 수 있음
for animal in animals:
    animal.sound()

