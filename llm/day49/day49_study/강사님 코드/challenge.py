# day49_challenge.py
# 여행 상담: 확정 사실 메모 + 최근 대화 보존

import json
from pathlib import Path
from util.print_util import pp, up

ROOT = Path(__file__).resolve().parent

# pairs: 질문/답변 튜플 리스트, facts: 확정 정보, recent_count: 보존 턴 수
def compile_context(pairs, facts, recent_count=2):
    if recent_count < 0:
        raise ValueError('recent_count는 0 이상이어야 합니다.')
    memo = ', '.join(f"{key}={value}" for key, value in facts.items())
    messages = [{'role': 'system', 'content': '여행 상담. 확인된 정보: ' + memo}]
    recent = pairs[-recent_count:] if recent_count else []
    for quetion, answer in recent:
        messages.append({'role': 'user', 'content': quetion})
        messages.append({'role': 'assistant', 'content': answer})
    return messages

def main():

    # 4턴에서 최근 2턴만 보존하되 예산과 목적지를 계속 유지

    pairs = [
        ("부산 여행을 갈게요.", "부산 여행 계획을 도와드리겠습니다."),
        ("예산은 20만원이에요.", "20만원 기준으로 제안하겠습니다."),
        ("대중교통을 이용해요.", "버스와 지하철 중심으로 정리하겠습니다."),
        ("마지막 날 코스를 추천해 주세요.", "해변과 시장을 추천합니다.")
    ]

    facts = {"도시": "부산", "예산": "20만원", "이동수단": "대중교통"}

    history = compile_context(pairs, facts, recent_count=2)

    assert '20만원' in history[0]['content'] # system메시지의 내용에 20만원 있는지 확인
    assert len(history) == 5 # history 길이가 5인지 확인

    path = ROOT / 'day49_trip.json'
    path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding='utf8')

    pp('확정 정보가 보존된 system: ', history[0]['content'])
    pp('최종 역할: ', [m['role'] for m in history])
    pp('저장: ', path)

if __name__ == '__main__':
    main()

up(5)























