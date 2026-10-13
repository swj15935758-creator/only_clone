# day33_basic.py
# [Basic: 쇼핑몰 고객 리뷰 토큰 빈도 분석]

import re
from collections import Counter
from util.print_util import pp

# 주제: 전자상거래 리뷰 정제와 빈도 집계 (강의의 AI·음성 예문 사용 금지)
#
# 데이터: [" 배송이 정말 빨라요!!! ", "포장이 깔끔하고 배송도 좋네요.",
#        "배송 늦음... 포장 불량", "상품 품질이 좋아요, 재구매!"]
#

DOCS = [
    " 배송이 정말 빨라요!!! ", "포장이 깔끔하고 배송도 좋네요.",
    "배송 늦음... 포장 불량", "상품 품질이 좋아요, 재구매!"
]

# 텍스트 정규화
# 1) 특수문자를 공백으로 바꾸고 중복 공백을 줄이세요.
def normalize(text):
    text = re.sub(r'[^가-힣A-Za-z0-9\s]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

# 문서 토큰화
# 2) 리뷰별 토큰 리스트를 출력하세요.
def inspect_document(document):
    cleaned = [normalize(text) for text in document]

    for index, doc in enumerate(cleaned, 1):
        tokens = doc.split()
        pp(f'{index}: {doc}')
        pp(f'tokens: {tokens}')

    return cleaned

# 3) 전체 단어 빈도 TOP 5를 출력하세요.
def frequency_top(n, cleaned):
    counts = Counter(' '.join(cleaned).split())
    pp(f'top{n}: {counts.most_common(n)}')
    return counts

# 4) 전체 리뷰 수와 고유 단어 수를 표시하세요.
def document_summary(cleaned, counts):
    pp(f'전체 리뷰 수: {len(cleaned)}')
    pp(f'고유 단어 수: {len(counts)}')

# 검증: 데이터 원본을 수정하지 않고 별도의 정제 리스트를 생성하세요.

if __name__ == '__main__':
    cleaned_docs = inspect_document(DOCS)
    counts = frequency_top(n=5, cleaned=cleaned_docs)
    document_summary(cleaned_docs, counts)