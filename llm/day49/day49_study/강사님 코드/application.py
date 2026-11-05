# day49_application.py
# 고객지원 대화를 한 쌍 단위로 유지하고 저장/복원 검증

import json
from pathlib import Path
from util.print_util import pp, up

ROOT = Path(__file__).resolve().parent

# history: 메시지 리스트, count: 유지할 최신 왕복 수
def recent_pairs(history, count=2):
    if not isinstance(count, int) or count<0:
        raise ValueError('count는 0이상의 정수여야 합니다.')
    system = [m for m in history if m['role'] == 'system'] # 시스템 메시지
    dialog = [m for m in history if m['role'] != 'system'] # 대화 메시지
    if len(dialog) % 2: # 홀수라면
        raise ValueError('질문이나 응답이 빠졌습니다.')
    for index in range(0, len(dialog), 2):
        if [m['role'] for m in dialog[index: index+2]] != ['user', 'assistant']:
            raise ValueError('user > assistant 순서가 아닙니다.')
    return system + (dialog[-2*count:] if count else [])

def main():

    history = [{'role': 'system', 'content': '쇼핑몰 지원 담당자'}]

    pairs = [
        ("배송은 언제인가요?", "주문 상태를 확인하세요."),
        ("교환 절차는요?", "교환 신청 메뉴를 이용하세요."),
        ("환불은 어떻게 하나요?", "환불 규정을 확인하세요."),
    ]

    for question, answer in pairs:
        history.extend([
            {'role': 'user', 'content': question},
            {'role': 'assistant', 'content': answer}
        ])

    recent = recent_pairs(history, 2) # 최근 2턴

    path = ROOT / 'day49_shop.json'
    path.write_text(json.dumps(recent, ensure_ascii=False, indent=2), encoding='utf-8')

    restored = json.loads(path.read_text(encoding='utf-8')) # JSON문자열 > Text
    assert restored == recent

    pp('원본 역할: ', [m['role'] for m in history])
    pp('축약 역할: ', [m['role'] for m in recent])

if __name__ == '__main__':
    main()