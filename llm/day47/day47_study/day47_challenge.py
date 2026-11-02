# day47_application.py
# 주제: 재난 상황 접수 메시지 우선 키워드 분석

import csv
import re
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from util.print_util import pp
from include.graph_config import set_graph

set_graph(10, 6, 12)

MESSAGES = [
    '건물 화재와 연기 발생',
    '엘리베이터에 사람 구조 요청',
    '주차장 연기 확인',
    '거리 가로등 고장 안내',
    '산불 화재 의심 신고',
    '구조 장비 지원 요청'
]

WORDS = ['화재', '연기', '구조']

QUERY = np.array([1.0, 1.0])

KEY_EMBEDDINGS = {
    '화재': [1.0, 0.2],
    '연기': [0.6, 0.3],
    '구조': [0.2, 1.0]
}

VALUES = {
    '화재': 5.0,
    '연기': 3.0,
    '구조': 4.0
}


def softmax(scores):
    scores = np.asarray(scores, dtype=float)
    shifted = scores - np.max(scores)
    exp_scores = np.exp(shifted)
    return exp_scores / np.sum(exp_scores)


def make_tokens(message):
    tokens = re.findall(r'[가-힣A-Za-z0-9]+', message)
    return list(dict.fromkeys(tokens))


def find_keywords(tokens):
    return [
        word for word in WORDS
        if any(word in token for token in tokens)
    ]


def calculate_priority(keywords):
    keyword_weights = {word: 0.0 for word in WORDS}

    if not keywords:
        return keyword_weights, 0.0

    keys = np.array(
        [KEY_EMBEDDINGS[word] for word in keywords],
        dtype=float
    )
    values = np.array(
        [VALUES[word] for word in keywords],
        dtype=float
    )

    scores = QUERY @ keys.T
    scaled_scores = scores / np.sqrt(keys.shape[1])
    weights = softmax(scaled_scores)
    priority = weights @ values

    for word, weight in zip(keywords, weights):
        keyword_weights[word] = float(weight)

    return keyword_weights, float(priority)


def analyze_messages():
    rows = []

    for message in MESSAGES:
        tokens = make_tokens(message)
        keywords = find_keywords(tokens)
        weights, priority = calculate_priority(keywords)

        row = {
            'message': message,
            'tokens': ' | '.join(tokens),
            'keywords': ' | '.join(keywords),
            '화재_weight': weights['화재'],
            '연기_weight': weights['연기'],
            '구조_weight': weights['구조'],
            'weight_sum': sum(weights.values()),
            'priority_score': priority
        }
        rows.append(row)

        pp('메시지:', message)
        pp('토큰 집합:', tokens)
        pp('긴급 키워드:', keywords)
        pp('키워드 가중치:', {
            word: round(weights[word], 3) for word in WORDS
        })
        pp('우선 점수:', round(priority, 3))

        if keywords:
            assert np.isclose(row['weight_sum'], 1.0)
        else:
            assert np.isclose(row['weight_sum'], 0.0)

    return rows


def save_csv(rows):
    path = Path(__file__).resolve().parent / 'dispatch_priority.csv'

    with path.open('w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    return path


def save_graph(rows):
    sorted_rows = sorted(rows, key=lambda row: row['priority_score'])
    messages = [row['message'] for row in sorted_rows]
    scores = [row['priority_score'] for row in sorted_rows]

    plt.figure()
    plt.barh(messages, scores, color='tomato')
    plt.xlabel('우선 점수')
    plt.title('재난 상황 접수 메시지 우선순위')
    plt.xlim(0, 5.5)
    plt.tight_layout()

    path = Path(__file__).resolve().parent / 'dispatch_priority.png'
    plt.savefig(path, dpi=150)
    plt.close()

    return path


def main():
    rows = analyze_messages()
    csv_path = save_csv(rows)
    graph_path = save_graph(rows)

    pp('CSV 저장:', csv_path)
    pp('그래프 저장:', graph_path)


if __name__ == '__main__':
    main()