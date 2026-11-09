# day52_application.py
# 주제:[APPLICATION 과제] 채용공고 기술스택 태깅

import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError # 통신에러, URL에러
from urllib.request import urlopen, Request # 요청, 연결 초기화
from dotenv import load_dotenv
from util.print_util import pp

ROOT = Path(__file__).resolve().parent

load_dotenv(ROOT / '.env') # 환경변수 로딩

# .env에서 모델명과 Ollama 서버 주소 읽기
MODEL = os.getenv('DAY52_MODEL', 'gemma3:1b') # 환경 변수키, 기본값
BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://127.0.0.1:11434')
BASE_URL = BASE_URL.rstrip('/') # 오른쪽에 만약 / 가 있으면 제거

POSTINGS = [
    "Python과 Pandas로 데이터 분석 서비스를 개발합니다.",
    "PostgreSQL 쿼리 작성과 Docker 배포 경험이 필요합니다.",
    "AWS 인프라 및 Kubernetes 운영을 담당합니다.",
]

EXAMPLES = [
    ("Python 자동화 개발", ["Python"]),
    ("SQL 기반 데이터 조회", ["SQL"]),
    ("Docker 이미지 배포", ["Docker"]),
    ("AWS 클라우드 서비스", ["AWS"]),
    ("Kubernetes 클러스터 운영", ["기타"]),
    ("Python과 Docker로 서버 개발", ["Python", "Docker"]),
]

LABELS = {'Python', 'SQL', 'Docker', 'AWS', '기타'}

# 검증용
EXPECTED = [
    ['Python', '기타'],
    ['SQL', 'Docker'],
    ['AWS', '기타'],
]

def zero_make_prompt(posting):
    header = (
        '당신은 개발자 채용공고에서 기술스택 태그를 추출하는 사람입니다.\n'
        '허용 태그는 Python, SQL, Docker, AWS, 기타입니다.\n'
        '한 공고에 여러 기술이 있으면 해당 태그를 모두 선택하세요.\n'
        'PostgreSQL은 SQL로 분류하세요.\n'
        'Pandas와 Kubernetes처럼 앞의 네 분류에 속하지 않는 기술은 기타로 분류하세요.\n'
        '공고에 없는 기술의 태그는 넣지 마세요.\n'
        '중복 태그 없이 {"tags": ["태그1", "태그2"]} 형태의 JSON 객체만 출력하세요.\n\n'
    )
    return header + f'채용공고: {posting}\n출력:'

def few_make_prompt(posting):
    header = (
        '당신은 개발자 채용공고에서 기술스택 태그를 추출하는 사람입니다.\n'
        '허용 태그는 Python, SQL, Docker, AWS, 기타입니다.\n'
        '한 공고에 여러 기술이 있으면 해당 태그를 모두 선택하세요.\n'
        'PostgreSQL은 SQL로 분류하세요.\n'
        'Pandas와 Kubernetes처럼 앞의 네 분류에 속하지 않는 기술은 기타로 분류하세요.\n'
        '공고에 없는 기술의 태그는 넣지 마세요.\n'
        '중복 태그 없이 {"tags": ["태그1", "태그2"]} 형태의 JSON 객체만 출력하세요.\n\n'
    )
    examples_text = ''.join(
        f'예시 입력: {sample}\n'
        f'예시 출력: {json.dumps({"tags": tags}, ensure_ascii=False)}\n'
        for sample, tags in EXAMPLES
    )
    return header + examples_text + f'\n채용공고: {posting}\n출력:'

def query_ollama(prompt, model):
    body = {
        'model': model,
        'prompt': prompt,
        'stream': False,
        'format': 'json',
        'options': {
            'temperature': 0,
            'num_predict': 200
        }
    }
    request = Request(
        f'{BASE_URL}/api/generate',
        data=json.dumps(body, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with urlopen(request, timeout=180) as response:
        result = json.load(response)
    return result['response']

def validate_item(raw):
    data = json.loads(raw)

    if not isinstance(data, dict) or set(data.keys()) != {'tags'}:
        raise ValueError('응답은 tags 필드 하나를 가진 JSON 객체여야 합니다.')

    tags = data['tags']

    if not isinstance(tags, list) or not tags:
        raise ValueError('tags에는 태그가 하나 이상 들어 있는 배열이 필요합니다.')

    for tag in tags:
        if not isinstance(tag, str) or tag not in LABELS:
            raise ValueError(f'허용되지 않은 태그입니다: {tag}')

    if len(tags) != len(set(tags)):
        raise ValueError('중복된 태그가 있습니다.')

    return tags

def main():
    results = []

    for strategy in ('zero', 'few'):
        if strategy == 'zero':
            pp('\n[ZERO-SHOT]')
        else:
            pp('\n[FEW-SHOT]')

        for index, posting in enumerate(POSTINGS):
            if strategy == 'zero':
                prompt = zero_make_prompt(posting)
            else:
                prompt = few_make_prompt(posting)

            pp(f'\n{index + 1}번 공고 프롬프트:')
            pp(prompt)

            try:
                raw = query_ollama(prompt, MODEL)
            except HTTPError as error:
                pp(f'Ollama HTTP 오류: {error.code} {error.reason}')
                pp(error.read().decode('utf-8', errors='replace'))
                return
            except (URLError, TimeoutError) as error:
                pp(f'Ollama 연결 오류: {error}')
                return

            pp(f'모델 원본 응답: {raw}')

            try:
                tags = validate_item(raw)
            except (ValueError, KeyError) as error:
                pp(f'{strategy} {index + 1}번 공고 검증 실패: {error}')
                results.append({
                    'strategy': strategy,
                    'posting': posting,
                    'raw': raw,
                    'tags': [],
                    'expected': EXPECTED[index],
                    'correct': False
                })
                continue

            correct = set(tags) == set(EXPECTED[index])

            results.append({
                'strategy': strategy,
                'posting': posting,
                'raw': raw,
                'tags': tags,
                'expected': EXPECTED[index],
                'correct': correct
            })

            pp(f'추출 태그: {tags}')
            pp(f'기준 태그: {EXPECTED[index]}')
            pp(f'일치 여부: {correct}')

    pp('\n전체 평가 결과:')
    pp(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()