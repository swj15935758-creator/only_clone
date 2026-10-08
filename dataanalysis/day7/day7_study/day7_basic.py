# day7_basic.py
from pathlib import Path

#1 day7_basic_data 폴더 생성
DIR_DATA = Path('day7_basic_data') # 파일 경로
DIR_DATA.mkdir(exist_ok=True)  # 폴더 생성 exist_ok=True 가 있으면 오류발생하지 않고 진행


#2 learning_log.txt 파일 생성
MEMO_PATH = DIR_DATA / 'learning_log.txt'
# 생성 및 텍스트 넣기
with open(MEMO_PATH, 'w', encoding='utf-8') as f:
    f.write('과정명:AI휴먼\n''오늘의 학습주제:파일입출력과 예외처리\n''오늘 이해한 핵심 개념 1개:with open()은 파일을 자동으로 닫아준다\n')
# 내용추가
with open(MEMO_PATH, 'a', encoding='utf-8') as f:
    f.write('다음에 복습할 내용\n')

with open(MEMO_PATH, 'r', encoding='utf-8') as f:
    print(f.read())













