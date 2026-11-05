# day49_basic.py
# 도서관 안내 메시지 구조와 JSON 저장

import json
from pathlib import Path
from util.print_util import pp, up

ROOT = Path(__file__).resolve().parent

ALLOWED = {'system', 'user', 'assistant'}

# history: 기록 리스트, question: 새 질문, answer: 응답 문자열
def append_pair(history, question, answer):
    result = list(history) # 기존 history 보호를 위해 복사
    result.extend([
        {'role': 'user', 'content': question},
        {'role': 'assistant', 'content': answer}
    ])
    for item in result:
        if item.get('role') not in ALLOWED:
            raise ValueError('지원하지 않는 역할입니다.')
        if not isinstance(item.get('content'), str):
            raise TypeError('content는 문자열이어야 합니다.')
    return result

def main():

    history = [{'role': 'system', 'content': '도서관 안내 도우미입니다.'}]
    history = append_pair(history, '열람실은 어디인가요?', '본관 3층입니다.')
    history = append_pair(history, '반납함은 어디인가요?', '1층 출입구입니다.')
    history = append_pair(history, '주말도 운영하나요?', '운영시간을 확인하세요.')

    path = ROOT / 'day49_library.json'
    path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding='utf-8')

    pp('역할: ', [item['role'] for item in history])
    pp('저장: ', path)

if __name__ == '__main__':
    main()