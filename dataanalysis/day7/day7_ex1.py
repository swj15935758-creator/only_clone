# day7_ex1.py
# 파일 입출력 예외처리 패키지모듈 import
import csv
# pathlin 모듈에서 Path 클래스 가져옴
from pathlib import  Path

# 1. 실습 폴더더와 메모파일 경로 생성
DATA_DIR = Path('day7_data') # 실습 폴더 경로
DATA_DIR.mkdir(exist_ok=True) # 폴더 생성 exist_ok = True: 폴더가 있다면 무시
MEMO_PATH = DATA_DIR / 'study_memo.txt' # 메모파일 경로

print(f'실습 폴더: {DATA_DIR}')
print(f'실습 폴더 위치: {DATA_DIR.resolve()}') # 실습 폴더의 절대 경로
print(f'메모파일 경로: {MEMO_PATH}')

# 2. 택스트 파일 새로 쓰기
first_text = 'AI 휴먼 7일차 학습 기록 \n 파일 입출력을 학습 합니다. \n'

#MEMO_PATH 경로의 파일을 쓰기모드로 열어서
with open(MEMO_PATH, 'w', encoding='utf-8') as f:
    f.write(first_text) # 문자열 파일에 씀

# 3. 텍스트 파일 이어 쓰기
append_text = '예외 처리와 모듈도 함께 학습합니다. \n'

# MEMO_PATH 경로의 파일을 추가 모드로 열어서
with open(MEMO_PATH, 'a', encoding='utf-8') as f:
    f.write(append_text)

# 4. 텍스트 파일 전체 읽기
with open(MEMO_PATH, 'r', encoding='utf-8') as f:
    print(f.read()) # 파일 전체를 읽어서 문자열로, 작은 파일에 유용

# 5. 텍스트 파일을 한줄씩 읽으며 줄번호화 같이표시
with open(MEMO_PATH, 'r', encoding='utf-8') as f:
    for line_number, line in enumerate(f, start=1):
        clean_line = line.strip() # 문자열의 앞뒤 공백 문자 제거
        print(f'{line_number}번째 라인: {clean_line}')

# 6. 텍스트 파일의 모든 줄을 요소로 하는 리스트
with open(MEMO_PATH, 'r', encoding='utf-8') as f:
    line_list = f.readlines()
    print(line_list)

### 어떤 언어, 프로그램을 만들던 예외는 무조건 처리해야함###

# 7. FileNotFoundError 예외처리

# 예외를 발생시키기위해 존재하지 않는 파일 경로를 생성
MISSING_PATH = DATA_DIR / 'missing.txt' #

# #예외처리를 안하는 경우
# with open(MISSING_PATH, 'r', encoding='utf-8') as f:
#     print(f.read())


try:
    with open(MISSING_PATH, 'r', encoding='utf-8') as f:
        print(f.read())
except FileNotFoundError: # 파일이 없다면 예외처리
    print('파일이 존재하지 않습니다! 확인해 주세요!')

print('예외처리 후 계속 수행할 코드')


# 8. ValueError  예외처리

try :
    score = int('90점')
except ValueError:
    print('정수로 변환 할 수 없는 문자열 입니다!')

print('예외처리 후 계속 수행할 코드')

# 9. try ~ except ~ else ~ finally 구문
number_text = '100'

try:
    number = int(number_text) # 예외 발생x
except ValueError:
    print('정수 변환이 불가능한 문자열 입니다!')
else: #예외가 발생하지 않았을때 실행할 구문 블럭
    print('정상적으로 수행됨!')
finally:
    print('예외발생 여부와 관계없이 수행됨!')
    print('주로 try블럭에서 사용된 자원을 해제할 필요가 있을떄 사용!')

# 10. package(패키지) 와 module(모듈)
# - 패키지 : 다른 패키지나 모듈을 포함하는 단위
# - 모듈 : 기능이나 역할로 구분해 둔 파이썬 파일
#       상수, 함수, 클래스들을 미리 만들어 두고 재사용할 목적으로 생성
# - 파이썬에서 패키지 생성법 : 폴더를 만들고 내용이 없는 __init__.py 파일을 만들어 둠
# - 모듈 임포트 방법
#   1) import 모듈명 : 모듈내의 상수, 함수, 클래스를 모두 가져옴
#   2) import 모듈명 as 별칭 : 모듈을 별칭으로 사용
#   3) from 모듈명 import 가져올 상수, 함수, 클래스들의 리스트
#       : 모듈에서 특정한 상수, 함수, 클래스만, 가져다 사용할때

import mypakage.mymodule as mn
print(mn.add(3,5))
print(mn.sub(3,5))

import mypakage.subpakage.submodule as sm
print(sm.mul(3,5))
print(sm.div(3,5))

from mypakage.mymodule import add, sub
print(add(3,5))
print(sub(3,5))

from mypakage.subpakage.submodule import mul , div
print(mul(3,5))
print(div(3,5))

# 11. CSV 파일 쓰기
# CSV 파일에 저장할 2차원 리스트
students = [
    ['name','score'],
    ['김민수',88],
    ['이서연',93],
    ['박지훈',76],
    ['최유진',85]
]

# CSV 파일경로 문자열
SCORE_PATH = DATA_DIR / 'score.csv'

with open(SCORE_PATH,'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f) # CSV 파일에 쓰는 writer
    writer.writerows(students)

# 12. CSV 파일 읽기

score_values = [] # 읽은 결과 저장할 리스트
with open(SCORE_PATH, 'r', encoding='utf-8') as f:
    reader = csv.reader(f) #CSV 파일 읽는 reader
    header = next(reader)  # 헤더라인 별도로 저장
    for row in reader:
        name = row[0] #이름
        score = int(row[1]) #성적
        score_values.append(score) #리스트에 추가
        print(f'{name}님 : {score}점')































