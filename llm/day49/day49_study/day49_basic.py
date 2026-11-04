# day49_basic.py
# 주제:대학 도서관 문의 대화 기록
# 목표: 역할별 메시지를 기록하고 저장하는 함수를 작성합니다.
import json
from pathlib import Path
from util.print_util import pp

ROOT = Path(__file__).resolve().parent

ROLE_SET = {'system', 'user', 'assistant'}

TOKENIZER_MODEL_ID = 'Qwen/Qwen2.5-0.5B-Instruct'

# 검사 함수 role/content 구조와 자료형 조건을 만족하는지 검사 하는 함수
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


# 호출 될때 마다 유저 어시스턴트 하나씩 쌍으로 추가 하는 함수
def append_pair(history, question, answer):
    result = list(history)
    result.append({'role': 'user', 'content': question})
    result.append({'role': 'assistant', 'content': answer})
    validate_messages(result)
    return result


# 메시지를 JSON 파일로 저장하는 함수
def save_json(messages, filename):
    validate_messages(messages)
    text = json.dumps(messages, ensure_ascii=False, indent=2)
    Path(filename).write_text(text, encoding='utf-8')


def main():
    history = [{'role': 'system', 'content': '도서관 안내 도우미입니다.'}]

    history = append_pair(history, '열람실은 어디인가요?', '본관 3층입니다.')
    history = append_pair(history, '반납함은 어디인가요?', '1층 출입구입니다.')
    history = append_pair(history, '주말도 운영하나요?', '운영시간을 확인하세요.')

    validate_messages(history)

    file_path = ROOT / 'day49_basic_history.json'
    save_json(history, file_path)

    pp('전체 역할 목록:', [message['role'] for message in history])
    pp('저장 경로:', file_path)


if __name__ == '__main__':
    main()