# day47_basic.py
# 주제:도서관 도서 제목 자동 분류

import csv
import re
from collections import Counter
from pathlib import Path
from util.print_util import pp

# [목표]
# - 도서 제목 8개를 준비하고 공백/정규식 기반 토큰화를 비교하세요.
# - 각 제목의 단어 수, 중복을 제외한 단어 수, 가장 빈도 높은 단어를
#   CSV(book_titles.csv)로 저장하고 차이를 설명하세요.

TITLES = [
    '파이썬 데이터 분석 실습', '파이썬 알고리즘 안내',
    '데이터 시각화 설계', '머신러닝 프로젝트 가이드',
    '프로젝트 분석 방법', '데이터 분석과 통계',
    '실전 파이썬 프로젝트', '머신러닝 데이터 입문'
]

# 공백 기반 토큰화 함수
def whitespace_split(titles):
    whitespace_text = []
    for title in titles:
        words = title.split()
        whitespace_text.append(words)
    return whitespace_text


# 정규식 기반 토큰화 함수
def normal_token(titles):
    normal_text = []
    for title in titles:
        words = re.findall(r'[가-힣A-Za-z0-9]+', title)
        normal_text.append(words)
    return normal_text

# 통계 분석 함수
def token_stats(words):
    counts = Counter(words)
    highest_count = max(counts.values(), default=0)
    top_words = [
        word for word, count in counts.items()
        if count == highest_count
    ]
    return len(words), len(counts), ', '.join(top_words), highest_count


def analyze_titles(titles):
    white_texts = whitespace_split(titles)
    normal_texts = normal_token(titles)
    rows = []

    for title, white_words, normal_words in zip(titles, white_texts, normal_texts):
        white_count, white_unique, white_top, white_frequency = token_stats(white_words)
        normal_count, normal_unique, normal_top, normal_frequency = token_stats(normal_words)

        rows.append({
            'title': title,
            'whitespace_tokens': ' , '.join(white_words),
            'whitespace_count': white_count,
            'whitespace_unique_count': white_unique,
            'whitespace_top_words': white_top,
            'whitespace_top_frequency': white_frequency,
            'regex_tokens': ' , '.join(normal_words),
            'regex_count': normal_count,
            'regex_unique_count': normal_unique,
            'regex_top_words': normal_top,
            'regex_top_frequency': normal_frequency,
            'different': white_words != normal_words
        })

    return rows


def compare_tokenization(rows):
    for row in rows:
        pp('제목:', row['title'])
        pp('공백 기반:', row['whitespace_tokens'])
        pp('정규식 기반:', row['regex_tokens'])
        pp('두 방식의 결과가 다른가:', row['different'])

    if all(not row['different'] for row in rows):
        pp('현재 제목에는 구두점이 없어 두 방식의 토큰화 결과가 같습니다.')
        pp('공백 방식은 띄어쓰기로 나누고, 정규식 방식은 글자와 숫자 묶음을 추출합니다.')
        pp('"파이썬/데이터 분석"처럼 구두점이 있으면 두 방식의 결과가 달라집니다.')


def save_csv(rows):
    path = Path(__file__).resolve().parent / 'basic_book_titles.csv'

    with path.open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    return path


def main():
    rows = analyze_titles(TITLES)
    compare_tokenization(rows)
    path = save_csv(rows)
    pp('CSV 저장:', path)


if __name__ == "__main__":
    main()