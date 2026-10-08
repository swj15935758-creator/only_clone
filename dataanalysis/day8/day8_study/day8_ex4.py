# day8_ex4.py
# dataclass

# dataclass는 데이터를 중심으로 하는 클래스에서 반복적으로 작성하던
# __init__, __repr__, __eq__ 등의 메서드를 자동 생성해 주는 클래스 데코레이터

from dataclasses import asdict, astuple, dataclass, field, FrozenInstanceError

def print_title(number: int, title: str) -> None:
    print(f"\n{'=' * 15} {number}. {title} {'=' * 15}")

# 1. 일반 클래스와 dataclass 비교
class NormalStudent:
    def __init__(self, name: str, age: int, score: int) -> None:
        self.name = name
        self.age = age
        self.score = score
    def __repr__(self) -> str:
        return (
            f"NormalStudent(name={self.name!r}, "
            f"age={self.age!r}, score={self.score!r})"
        )
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NormalStudent):
            return NotImplemented
        return (
            self.name == other.name
            and self.age == other.age
            and self.score == other.score
        )

# @dataclass가 반복적인 특수 메서드를 자동 생성합니다.
@dataclass
class Student:
    name: str
    age: int
    score: int

normal_student = NormalStudent("홍길동", 25, 90)
student1 = Student("홍길동", 25, 90)
student2 = Student(name="홍길동", age=25, score=90)

print("일반 클래스:", normal_student)
print("dataclass 객체:", student1)       # 자동 생성된 __repr__ 사용
print("필드 값 비교:", student1 == student2)  # 자동 생성된 __eq__ 사용

# 2. 기본값, 필드 순서, 사용자 정의 메서드
@dataclass
class CourseResult:
    # 기본값이 없는 필드는 기본값이 있는 필드보다 앞에 선언해야 함
    student_name: str
    python_score: int
    ai_score: int
    attendance: int = 100
    # 두 과목 총점 반환
    def total(self) -> int:
        return self.python_score + self.ai_score
    # 두 과목 평균 반환
    def average(self) -> float:
        return self.total() / 2
    # 합격여부 반환
    def is_passed(self) -> bool:
        return self.average() >= 60 and self.attendance >= 80

result = CourseResult("김코딩", 85, 92)
print(result)
print("총점:", result.total())
print(f"평균: {result.average():.1f}")
print("수료 여부:", result.is_passed())

# 3. 가변 객체의 기본값: field(default_factory=...)
@dataclass
class Learner:
    name: str
    # list, dict, set 같은 가변 객체는 default_factory로 생성합니다.
    # Learner 객체가 생성될 때마다 새로운 리스트가 만들어집니다.
    skills: list[str] = field(default_factory=list)

    def add_skill(self, skill: str) -> None:
        if skill not in self.skills:
            self.skills.append(skill)

learner1 = Learner("이파이")
learner2 = Learner("박데이터")
learner1.add_skill("Python")
learner1.add_skill("SQL")

print(learner1)
print(learner2)  # learner1의 리스트와 공유되지 않으므로 빈 리스트
print("서로 다른 리스트인가?", learner1.skills is not learner2.skills)

# 4. __post_init__: 자동 생성된 __init__ 직후의 검증과 계산
@dataclass
class Product:
    name: str
    price: int
    quantity: int = 1
    # init=False: 객체 생성 시 인자로 받지 않는 필드
    total_price: int = field(init=False)

    # 자동 생성된 __init__ 실행 직후 자동 호출됨
    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("상품명은 비워 둘 수 없습니다.")
        if self.price < 0:
            raise ValueError("가격은 0 이상이어야 합니다.")
        if self.quantity < 1:
            raise ValueError("수량은 1 이상이어야 합니다.")
        self.total_price = self.price * self.quantity

product = Product("무선 키보드", 45_000, 2)
print(product)
print(f"결제 금액: {product.total_price:,}원")

try:
    invalid_product = Product("마우스", -10_000)
except ValueError as error:
    print("검증 오류:", error)

# 5. frozen=True: 생성 후 필드 변경을 제한하는 값 객체
@dataclass(frozen=True)
class Point:
    x: int
    y: int

point = Point(10, 20)
print(point)

try:
    point.x = 100  # 실행 시 FrozenInstanceError 발생
except FrozenInstanceError as error:
    print("변경 제한 확인:", type(error).__name__)

# 6. dataclass 객체를 dict와 tuple로 변환
# asdict(객체) 함수 : 객체를 딕셔너리로 변환
# astuple(객체) 함수 : 객체를 튜플로 변환
# JSON으로 변환하려면 먼저 asdict()로 변환한 뒤 json.dumps()를 사용
student_dict = asdict(student1)
student_tuple = astuple(student1)

print("딕셔너리 변환:", student_dict)
print("튜플 변환:", student_tuple)

# 7. 정리: dict, dataclass, 일반 class의 선택 기준
# dict : 구조가 단순하거나 자주 달라지는 임시 데이터
# dataclass
# - 필드 구조가 명확한 데이터 중심 객체
# - DTO, 설정, 좌표, 주문 항목, 분석 결과 등에 적합
# - __init__, __repr__, __eq__의 반복 코드를 줄이고 싶을 때
# 일반 class
# - 복잡한 상태 관리와 비즈니스 행위가 중심인 객체
# - 생성 과정과 속성 제어를 세밀하게 설계해야 할 때