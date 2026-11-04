# day49_application.py
# 주제:쇼핑몰 고객지원 최근 대화 관리
# 목표: 주문 문의 대화를 완성된 왕복 단위로 관리합니다.
import json
from pathlib import Path
from util.print_util import pp

ROOT = Path(__file__).resolve().parent
ROLE_SET = {'system', 'user', 'assistant'}
TOKENIZER_MODEL_ID = 'Qwen/Qwen2.5-0.5B-Instruct'

# 요구사항
# 1. 배송 문의/교환 문의/환불 문의 3턴 예시를 구성합니다.
# 2. system을 유지하면서 최근 2턴만 남기는 함수를 구현합니다.
# 3. 누락된 assistant 답변을 만나면 ValueError를 발생시킵니다.
# 4. 원본과 축약 기록의 역할 목록을 출력합니다.
# 5. JSON 저장 및 재로드 후 내용이 같은지 검증합니다.
#
# 완료 조건: 출력 메시지가 system 1개와 왕복 대화 2개입니다.

# 각 메세지가 role/content 구조와 자료형 조건을 만족하는지 검사하는 함수
# 반환값: 모든 메세지가 올바르면 True, 오류가 있으면 예외 발생
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

# 메시지를 JSON 파일로 저장하는 함수
def save_json(messages, filename):
    validate_messages(messages)
    text = json.dumps(messages, ensure_ascii=False, indent=2)
    Path(filename).write_text(text, encoding='utf-8')

# 호출 될때 마다 유저 어시스턴트 하나씩 쌍으로 추가 하는 함수
def append_pair(history, question, answer):
    result = list(history)
    result.append({'role': 'user', 'content': question})
    result.append({'role': 'assistant', 'content': answer})
    validate_messages(result)
    return result

# system 메세지와 최근 완성된 질문/응답 쌍만 남기는 함수
# max_turns: 남길 최근 질문/응답 쌍의 개수
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

def main():
    result = [{'role': 'system', 'content': '넌 쇼핑몰 고객지원 도우미야'}]

    pairs = [
        ("배송은 언제인가요?", "주문 상태를 확인하세요."),
        ("교환 절차는요?", "교환 신청 메뉴를 이용하세요."),
        ("환불은 어떻게 하나요?", "환불 규정을 확인하세요."),
    ]

    for question, answer in pairs:
        result = append_pair(result, question, answer)

    recent = keep_recent_turns(result, max_turns=2)

    pp('원본 역할 목록:', [message['role'] for message in result])
    pp('축약 역할 목록:', [message['role'] for message in recent])

    try:
        keep_recent_turns(result[:-1], max_turns=2)
    except ValueError as error:
        pp('assistant 답변 누락 검사:', error)

    file_path = ROOT / 'application.json'
    save_json(recent, file_path)

    loaded = json.loads(file_path.read_text(encoding='utf-8'))
    if loaded != recent:
        raise ValueError('저장한 내용과 다시 읽은 내용이 다릅니다.')

    pp('저장 후 재로드 결과 일치:', loaded == recent)
    pp('저장 경로:', file_path)

if __name__ == '__main__':
    main()