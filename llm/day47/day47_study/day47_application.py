# day47_application.py
# 주제:온라인 쇼핑 리뷰의 키워드 주목도
#
# [목표]
# 전자기기 사용후기 5문장을 준비하세요.

import csv
import re
from pathlib import Path
import numpy as np
from util.print_util import pp

REVIEWS = [
    '배터리 배터리 화면', '배송이 빠르고 화면이 선명해요',
    '화면 크기가 좋지만 배터리는 아쉬워요',
    '배송 배송이 너무 느립니다', '제품의 외관은 깔끔합니다'
]

KEYWORDS = ['배터리', '화면', '배송']


def softmax(scores):
    scores = np.asarray(scores, dtype=np.float32)
    shifted = scores - np.max(scores, axis=-1, keepdims=True)
    exp_scores = np.exp(shifted)
    return exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)


# 지정 키워드(배터리, 화면, 배송)의 출현 위치에 따라 가중치를 계산하고
def one_query_attention(q, k, v):
    q = np.asarray(q, dtype=float)
    k = np.asarray(k, dtype=float)
    v = np.asarray(v, dtype=float)

    dot_scores = q @ k.T
    scaled_scores = dot_scores / np.sqrt(k.shape[1])
    weights = softmax(scaled_scores)
    context = weights @ v

    pp('Q@K.T(내적):', dot_scores)
    pp('np.sqrt(d_k)로 나눈 점수:', np.round(scaled_scores, 3))
    pp('Softmax 가중치:', np.round(weights, 3))
    pp('가중치 합계:', weights.sum())
    pp('Context Vector:', np.round(context, 3))

    return weights, context


def keyword_features(review):
    features = []
    present_indices = []

    for index, keyword in enumerate(KEYWORDS):
        positions = [
            match.start()
            for match in re.finditer(re.escape(keyword), review)
        ]

        if positions:
            count = len(positions)
            position_score = sum(1 / (position + 1) for position in positions)
            features.append([count, position_score])
            present_indices.append(index)

    return features, present_indices


def review_keyword_weights(review):
    features, present_indices = keyword_features(review)

    if not present_indices:
        return np.zeros(len(KEYWORDS)), 1.0

    q = np.array([1., 1.])
    k = np.array(features, dtype=float)
    v = np.eye(len(KEYWORDS))[present_indices]

    _, keyword_weights = one_query_attention(q, k, v)
    return keyword_weights, 0.0


# softmax로 리뷰별 키워드 주목도 확률을 구하세요.
# 확률 행의 합이 1인지 검사하고 CSV(review_weights.csv)로 저장하세요.
def analyze_reviews():
    rows = []

    for review in REVIEWS:
        pp('리뷰:', review)
        keyword_weights, other_weight = review_keyword_weights(review)
        total = float(keyword_weights.sum() + other_weight)

        if not np.isclose(total, 1.0):
            raise ValueError(f'가중치 합계가 1이 아닙니다: {review}')

        row = {'review': review}
        for keyword, weight in zip(KEYWORDS, keyword_weights):
            row[keyword] = round(float(weight), 4)

        row['기타'] = round(float(other_weight), 4)
        row['합계'] = round(total, 4)
        rows.append(row)

        pp('리뷰별 가중치:', row)

    return rows


def save_review_weights_csv(rows):
    path = Path(__file__).resolve().parent / 'review_weights.csv'

    with path.open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=['review'] + KEYWORDS + ['기타', '합계']
        )
        writer.writeheader()
        writer.writerows(rows)

    return path


def main():
    rows = analyze_reviews()
    path = save_review_weights_csv(rows)
    pp('CSV 저장:', path)


if __name__ == '__main__':
    main()