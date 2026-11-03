# day47_basic.py
# 도서 제목에 대한 단어 기반 토큰 빈도 분석

import csv
import re
from collections import Counter
from pathlib import Path
from util.print_util import pp, up

ROOT = Path(__file__).resolve().parent

TITLES = [
    '파이썬 데이터 분석 실습', '파이썬 알고리즘 안내',
    '데이터 시각화 설계', '머신러닝 프로젝트 가이드',
    '프로젝트 분석 방법', '데이터 분석과 통계',
    '실전 파이썬 프로젝트', '머신러닝 데이터 입문'
]

# 한글, 영문, 숫자 추출 함수
def tokenize(text):
    return re.findall(r'[가-힣A-Za-z0-9]+', text.lower())

def main():

    path = ROOT / 'book_titles.csv'

    with path.open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['title', 'space_count', 'regex_count', 'unique_count', 'most_common'])
        for title in TITLES:
            tokens = tokenize(title)
            counts = Counter(tokens) # 토큰과 토큰 빈도수 딕셔너리
            frequent = counts.most_common(1)[0][0] if counts else ''
            writer.writerow([title, len(title.split()), len(tokens), len(counts), frequent])
            pp(title, tokens, '최빈: ', frequent)

    pp('저장: ', path)

if __name__ == '__main__':
    main()

up(5)











