# day2_challenge.py
# AI휴먼과정Day2 - Challenge과제
# [과제명]
# 자료형오류찾아수정하기 - 다음일차형변환미리보기

# [목표]
# type()을이용해자료형을확인하고, 문자열과숫자를혼동했을때생기는문제를찾아수정합니다.

# ※ 형변환(TypeCasting)은Day3에서본격학습하므로오늘은최소한의예고수준으로진행합니다.

# [권장 시간]
# 30~40분

# [문제 상황]
# 아래데이터는외부입력에서들어왔다고가정합니다.

raw_age = "25"
raw_score = "91.5"
raw_name = "홍길동"
raw_portfolio_url = None

age = raw_age
score = raw_score
name = raw_name
portfolio_url = raw_portfolio_url
# [수행 과제] raw_age, raw_score, name의자료형을type()으로출력하세요.아래잘못된형변환사례2개를수정하세요.
type_check = f'{type(age)}\n {type(score)}\n {type(name)}'
print(type_check)

age = raw_age
score = raw_score
name = raw_name

age= int(25)        #str > int
score = float(91.5)    #str > float
name = "홍길동"

type_check = f'{type(age)}\n {type(score)}\n {type(name)}'
print(type_check)
# 사례 A: age = float(raw_age)나이는정수로관리하고싶습니다.더적절한형변환으로수정하세요.
# 사례 B: score = int(raw_score)"91.5"는소수점이포함된문자열이라int("91.5")는바로변환할수없습니다.
# 실수점수를유지하도록수정하세요.수정한age와score의값과자료형을출력하세요.
# 다음문장을f - string으로출력하세요. "홍길동님의 나이는 25세이고 사전점수는 91.5점입니다."
print(f'{name}님의 나이는 {age}세이고 사전점수는  {score} 입니다.')
# 코드주석으로다음질문에답하세요."25"와25는무엇이다른가?
# "25" 는 str 이고 25는 int 형 자료라서 다른다

# type()을먼저확인하면어떤점이좋은가?
# 원하지 않는 타입의 변화를 막고 원하는 타입의 사용이 가능하다

# 선택심화: None값을가진portfolio_url변수를하나만들고type()결과를출력하세요.
print(type(portfolio_url))

# [주의] 아직try/ except 예외처리는 배우지 않았으므로 사용하지 않아도 됩니다.오늘의핵심은오류를 ‘막는기술’보다자료형을 ‘확인하는습관’입니다.
# 기억이 안남


# [평가 포인트] raw데이터가str임을확인했는가?       > 확인함
# age를int로바르게변환했는가?                     > 했음
# score를float로바르게변환했는가?                 > 했음
# 수정후 type()으로결과를재확인했는가?               > 재차 확인함
# 문자열과숫자의차이를말로설명할수있는가?              > 문자열은 숫자 문자가 붙어있는것 정수와 실수는 숫자를 계산할 수 있는것
