# day52_basic.py
# 주제:[BASIC 과제] 회의록 액션아이템 추출

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

NOTES = [
    "민지가 API 명세를 금요일까지 정리하기로 했다.",
    "지훈이 발표자료를 작성하기로 했으며 일정은 미정이다.",
]

def build_prompt(message):
    header = (
        '당신은 회의 메모에서 실행할 업무를 추출하는 사람입니다.\n'
        '다음 회의 메모 한 건에서 담당자, 업무, 기한을 찾으세요.\n'
        '정보가 없는 필드는 "미정"으로 기록하세요.\n'
        '결과는 원소가 하나인 JSON 배열로 출력하세요.\n'
        '배열 안 객체의 키는 "담당자", "업무", "기한"만 사용하세요.\n'
        '설명이나 마크다운 없이 JSON만 출력하세요.\n\n'
        '회의 메모:\n'
    )
    return header + message

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

    if isinstance(data, list):
        if len(data) != 1:
            raise ValueError('메모 한 건에 대한 결과가 한 개가 아닙니다.')
        item = data[0]
    elif isinstance(data, dict):
        if isinstance(data.get('items'), list):
            if len(data['items']) != 1:
                raise ValueError('메모 한 건에 대한 결과가 한 개가 아닙니다.')
            item = data['items'][0]
        else:
            item = data
    else:
        raise ValueError('모델 응답이 JSON 객체 또는 배열이 아닙니다.')

    required_keys = {'담당자', '업무', '기한'}

    if not isinstance(item, dict) or set(item.keys()) != required_keys:
        raise ValueError('담당자, 업무, 기한 필드를 확인하세요.')

    for key in required_keys:
        if not isinstance(item[key], str) or not item[key].strip():
            raise ValueError(f'{key} 필드에 값이 없습니다.')

    return item

def main():
    items = []

    try:
        for number, note in enumerate(NOTES, start=1):
            prompt = build_prompt(note)
            raw = query_ollama(prompt, MODEL)

            pp(f'{number}번 메모 원본 응답: {raw}')

            item = validate_item(raw)
            items.append(item)

        if items[1]['기한'] != '미정':
            raise ValueError('두 번째 메모의 기한은 미정이어야 합니다.')

    except HTTPError as error:
        pp(f'Ollama HTTP 오류: {error.code} {error.reason}')
        detail = error.read().decode('utf-8', errors='replace')
        pp(f'상세 오류: {detail}')
        return
    except (URLError, TimeoutError) as error:
        pp(f'Ollama 연결 오류: {error}')
        return
    except (ValueError, KeyError) as error:
        pp(f'응답 검증 오류: {error}')
        return

    pp('최종 추출 결과:')
    pp(json.dumps(items, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()