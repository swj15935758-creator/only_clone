# day49_challenge.py
# 주제:여행 일정 상담 맥락 메모
# 목표: 여행 일정 서비스에 요약 메모 + 최근 2턴 정책을 구현합니다.

import json
from pathlib import Path
from util.print_util import pp

ROOT = Path(__file__).resolve().parent
ROLE_SET = {'system', 'user', 'assistant'}
TOKENIZER_MODEL_ID = 'Qwen/Qwen2.5-0.5B-Instruct'
MAX_TURNS = 4

# 검증 함수
def validate_messages(messages):
    if not isinstance(messages, list):
        raise TypeError('messages는 리스트여야 합니다')
    for index, message in enumerate(messages):
        if not isinstance(message, dict):
            raise TypeError(f'{index}번 메세지는 딕셔너리여야 합니다.')
        if message.get('role') not in ROLE_SET:
            raise ValueError(f'{index}번 메세지의 역할이 올바르지 않습니다.')
        if not isinstance(message.get('content'), str):
            raise TypeError(f'{index}번 메세지는 문자열이어야 합니다.')
    return True

# 턴추가 함수
def add_turn(messages, question, answer):
    result = list(messages)
    result.append({'role': 'user', 'content': question})
    result.append({'role': 'assistant', 'content': answer})
    validate_messages(result)
    return result

# 턴 보존 함수
def keep_recent_turns(messages, max_turns=2):
    validate_messages(messages)
    if isinstance(max_turns, bool) or not isinstance(max_turns, int):
        raise TypeError('max_turns는 정수여야 합니다.')
    if max_turns < 0:
        raise ValueError('max_turns는 0 이상이어야 합니다.')

    system = [m for m in messages if m['role'] == 'system']
    dialog = [m for m in messages if m['role'] != 'system']

    if len(dialog) % 2 or any(
        dialog[i]['role'] != 'user' or dialog[i + 1]['role'] != 'assistant'
        for i in range(0, len(dialog), 2)
    ):
        raise ValueError('대화 기록은 완성된 user/assistant 쌍으로 구성되어야 합니다.')

    return system + (dialog[-2 * max_turns:] if max_turns else [])

# Json저장 함수
def save_json(messages, filename):
    validate_messages(messages)
    text = json.dumps(
        messages,
        ensure_ascii=False,
        indent=2
    )
    Path(filename).write_text(text, encoding='utf-8')

def main():
    pairs = [
        ("부산 여행을 갈게요.", "부산 여행 계획을 도와드리겠습니다."),
        ("예산은 20만원이에요.", "20만원 기준으로 제안하겠습니다."),
        ("대중교통을 이용해요.", "버스와 지하철 중심으로 정리하겠습니다."),
        ("마지막 날 코스를 추천해 주세요.", "해변과 시장을 추천합니다."),
    ]

    result = [
        {'role': 'system', 'content': '넌 여행 일정 메모 도우미야.'}
    ]

    for question, answer in pairs:
        result = add_turn(result, question, answer)

    facts = {"도시": "부산", "예산": "20만원", "이동수단": "대중교통"}
    fact_text = ', '.join(
        f'{key}: {value}' for key, value in facts.items()
    )
    result[0]['content'] += '\n확인된 정보: ' + fact_text
    # pp(result) # 확인용
    recent = keep_recent_turns(result, max_turns=2)

    assert len(pairs) == MAX_TURNS
    assert len(recent) == 5
    assert '예산: 20만원' in recent[0]['content']

    file_path = ROOT / 'day49_challenge.json'
    save_json(recent, file_path)

    # 실제 토큰 수가 필요하면 Chat Template로 recent를 토큰화할 수 있습니다.
    pp('원본 역할:', [message['role'] for message in result])
    pp('최근 역할:', [message['role'] for message in recent])
    pp('남은 system 본문:', recent[0]['content'])
    pp('저장 경로:', file_path)


if __name__ == '__main__':
    main()