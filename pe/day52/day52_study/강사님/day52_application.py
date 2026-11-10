# day52_application.py
# 주제:[APPLICATION 과제] 채용공고 기술스택 태깅

# [업무 상황]
# 개발자 채용공고에서 Python/SQL/Docker/AWS/기타 기술 분류 태그를 추출합니다.
#
# [구현 요구사항]
# Zero-shot과 Few-shot을 각각 작성합니다.
# 예시에는 최소 3개 다른 기술 분류를 포함하고 실제 공고 3건에 대해 두 프롬프트를 생성합니다.
#
# [조건]
# 기존 실습의 쇼핑몰 고객 문의 데이터와 코드를 재사용하지 마세요.
# 함수형 Python 코드로 작성하고 핵심 함수·파라미터를 설명하세요.
# 실제 LLM 호출을 사용하지 않는 경우 시뮬레이션임을 명시하세요.
# 출력 구조와 검증 방법을 명확히 제시하세요.

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

# 프롬프트 생성 함수
# text: 채용공고
# strategy: zero 또는 few 선택
def make_prompt(text, strategy):
    if strategy not in ('zero', 'few'):
        raise ValueError('strategy 는 zero 또는 few 이어야 합니다.')
    lines = [
        '채용공고의 요구 기술을 추출하세요.',
        '허용태그: Python, SQL, Docker, AWS, 기타',
        '복수 태그는 쉼표로 구분하고 중복은 제거하세요.',
        '예시에 없는 기술만 나타나면 기타를 사용하세요.'
    ]
    if strategy == 'few': # few-shot
        for source, tag in EXAMPLES:
            lines.append(f'예시:{source}=>{tag}')
    lines.append(f'<공고>{text}</공고>\n결과:')
    return '\n'.join(lines) # 줄바꿈이 포함된 전체 한 문장으로 리턴

def main():
    for strategy in ('zero', 'few'):
        for text in POSTINGS:
            pp(f'[{strategy}]\n{make_prompt(text, strategy)}\n')

if __name__ == '__main__':
    main()