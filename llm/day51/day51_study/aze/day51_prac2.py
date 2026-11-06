# day51_prac2.py

import json
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import streamlit as st
from openai import OpenAI, OpenAIError
from kiwipiepy import Kiwi

kiwi = Kiwi()
ROOT = Path(__file__).resolve().parent
load_dotenv(dotenv_path=ROOT / '.env')

# 문제는 총 5개, 매 문제마다 GPT가 1개씩 생성
MAX_QUIZ = 5
# 답변 기회는 문제당 2회
MAX_SUBMIT = 2


# 첫 시도 정답 20점, 두 번째 정답 10점
# 힌트 사용 시 획득 점수에서 5점 차감 (최소 0점)
# 2번 틀리면 정답과 해설 공개, 다음 문제로 이동
# 정답은 GPT를 다시 호출하지 않고, 처음 생성한 정답과 Python 문자열 비교
# 최고 점수는 100점


# OpenAI API 클라이언트 생성 함수
def make_client(api_key):
    return OpenAI(api_key=api_key, timeout=30.0, max_retries=1)


# GPT에게 문제 물어보는 함수
def ask_quiz(client, model, question):
    instructions = (
        '당신은 한국어 개그 퀴즈 출제자입니다. '
        '한국에서 실제로 통용되는 사람의 개그의 방식을 이해하고 문제를 생성하세요. '

        '억지스러운 언어유희는 절대 출제하지 마세요. '
        '단어 사이에 실제로 존재하지 않는 발음이나 의미 관계를 만들어내지 마세요. '
        '정답을 먼저 정한 뒤 억지 해설을 붙이는 것은 금지합니다. '
        '단어 끼리의 억지스러운 융합은 금지합니다. '

        '말장난을 설명하기 어렵다면 해당 문제는 버리고 다시만들어서 보내세요. '

        'question은 문제, answer는 짧은 정답, '
        'hint는 정답을 직접 공개하지 않는 힌트, '
        'explanation은 실제 발음 또는 의미의 연결을 설명하는 해설입니다. '
        '해설에 재밌다고 적어도 재미가 있는게 아님'

        '이전에 출제한 문제와 중복되지 않게 하고 '
        '반드시 지정된 JSON Schema로 응답하세요.'
    )

    payload = {
        '이전에_출제한_문제': question,
        '요청': '새로운 한국어 아재개그 퀴즈 1개를 출제해 주세요.'
    }

    schema = {
        'type': 'object',
        'properties': {
            'question': {'type': 'string'},
            'answer': {'type': 'string'},
            'hint': {'type': 'string'},
            'explanation': {'type': 'string'}
        },
        'required': ['question', 'answer', 'hint', 'explanation'],
        'additionalProperties': False
    }

    # ChatGPT 응답 획득
    response = client.responses.create(
        model=model,
        instructions=instructions,
        input=json.dumps(payload, ensure_ascii=False),
        text={
            'format': {
                'type': 'json_schema',
                'name': 'quiz',
                'strict': True,
                'schema': schema
            }
        },
        max_output_tokens=500,
        store=False
    )

    raw = (response.output_text or '').strip()
    if not raw:
        raise ValueError('GPT가 문제를 반환하지 않았습니다.')

    quiz = json.loads(raw)
    if not isinstance(quiz, dict) or set(quiz) != set(schema['required']):
        raise ValueError('문제 JSON의 키가 올바르지 않습니다.')

    for key in schema['required']:
        if not isinstance(quiz[key], str) or not quiz[key].strip():
            raise ValueError(f'{key} 값이 비어 있거나 문자열이 아닙니다.')
        quiz[key] = quiz[key].strip()

    usage = response.usage
    in_tokens = getattr(usage, 'input_tokens', 0) if usage else 0
    out_tokens = getattr(usage, 'output_tokens', 0) if usage else 0
    return quiz, in_tokens, out_tokens


def validate_answer_word(answer):
    if not isinstance(answer, str) or not answer.strip():
        return False, '정답이 비어 있음'

    answer = answer.strip()

    if any(char.isspace() for char in answer):
        return False, '정답에 공백이 포함됨'

    if not answer.isalnum():
        return False, '정답에 특수문자가 포함됨'

    tokens = kiwi.tokenize(answer)

    if not tokens:
        return False, '형태소 분석 결과가 없음'

    if any(token.tag in ('EF', 'EC') for token in tokens):
        return False, '문장형 정답일 가능성이 있음'

    return True, '기본 형식 검사 통과'


# 스트림릿에서 세션 스테이트를 초기화하는 함수
def init_state():
    defaults = {
        'question_name': 'LLM 아재퀴즈 게임',
        'question': '',
        'quiz_data': None,
        'quiz_index': 1,
        'attempts': 0,
        'hint_used': False,
        'answered': False,
        'finished': False,
        'score': 0,
        'log': [],
        'actions': 0,
        'result': '',
        'input_tokens': 0,
        'output_tokens': 0,
        'kiwi_checks': [],
    }
    for name, value in defaults.items():
        if name not in st.session_state:
            st.session_state[name] = value


# 새로운 다섯 문제 시작하고 기존 기록을 초기화
def start_quiz(name):
    st.session_state['question_name'] = name
    st.session_state['question'] = ''
    st.session_state['quiz_data'] = None
    st.session_state['quiz_index'] = 1
    st.session_state['attempts'] = 0
    st.session_state['hint_used'] = False
    st.session_state['answered'] = False
    st.session_state['finished'] = False
    st.session_state['score'] = 0
    st.session_state['log'] = []
    st.session_state['actions'] = 0
    st.session_state['result'] = ''
    st.session_state['input_tokens'] = 0
    st.session_state['output_tokens'] = 0
    st.session_state['kiwi_checks'] = []
    for key in list(st.session_state.keys()):
        if key.startswith('answer_input_'):
            del st.session_state[key]


# 띄어쓰기 차이는 무시하고 같은 답인지 검사
def normalize_answer(text):
    return ''.join(text.split()).casefold()


# 사용자가 제출한 정답을 Python으로 판정하는 함수
def answer_quiz(question):
    if not question.strip():
        return False, '정답을 입력하세요.'

    quiz = st.session_state['quiz_data']
    if quiz is None or st.session_state['answered']:
        return False, '현재 제출할 수 있는 문제가 없습니다.'

    st.session_state['attempts'] += 1
    st.session_state['actions'] += 1
    correct = normalize_answer(question) == normalize_answer(quiz['answer'])

    if correct:
        points = 20 if st.session_state['attempts'] == 1 else 10
        if st.session_state['hint_used']:
            points = max(0, points - 5)
        st.session_state['score'] += points
        st.session_state['answered'] = True
        st.session_state['result'] = f'정답입니다! {points}점을 획득했습니다.'
    elif st.session_state['attempts'] >= MAX_SUBMIT:
        points = 0
        st.session_state['answered'] = True
        st.session_state['result'] = '아쉽네요! 두 번 모두 틀렸습니다.'
    else:
        return False, '아쉽네요! 한 번 더 도전해 보세요.'

    st.session_state['log'].append({
        'number': st.session_state['quiz_index'],
        'question': quiz['question'],
        'answer': quiz['answer'],
        'hint_used': st.session_state['hint_used'],
        'attempts': st.session_state['attempts'],
        'correct': correct,
        'points': points,
        'submitted_answer': question.strip(),
        'played_at': datetime.now().isoformat(timespec='seconds')
    })
    return correct, st.session_state['result']


# 다음 문제를 시작하거나 다섯 문제의 결과 화면으로 이동
def next_quiz():
    if st.session_state['quiz_index'] >= MAX_QUIZ:
        st.session_state['finished'] = True
        return

    st.session_state['quiz_index'] += 1
    st.session_state['question'] = ''
    st.session_state['quiz_data'] = None
    st.session_state['attempts'] = 0
    st.session_state['hint_used'] = False
    st.session_state['answered'] = False
    st.session_state['result'] = ''


def main():
    st.set_page_config(page_title='LLM 아재퀴즈 게임', layout='centered')
    init_state()

    st.title('LLM 아재퀴즈 게임')
    st.caption('총 5문제 · 문제당 기회 2번 · 힌트 사용 시 5점 감점')

    if st.button('새 게임'):
        start_quiz('LLM 아재퀴즈 게임')
        st.rerun()

    st.write('현재 점수')
    st.header(f"{st.session_state['score']}점")

    if st.session_state['finished']:
        st.subheader('게임 종료')
        st.success(f"최종 점수: {st.session_state['score']} / 100점")
        st.write(f"완료한 문제: {len(st.session_state['log'])}/{MAX_QUIZ}")
        for row in st.session_state['log']:
            with st.expander(f"문제 {row['number']}: {row['question']}"):
                st.write('정답:', row['answer'])
                st.write('결과:', '정답' if row['correct'] else '오답')
                st.write('획득 점수:', row['points'])
        st.caption(f"누적 토큰: 입력 {st.session_state['input_tokens']:,} / 출력 {st.session_state['output_tokens']:,}")
        with st.expander('Kiwi 실험 기록'):
            for check in st.session_state['kiwi_checks']:
                st.write(f"문제 {check['number']} / 정답: {check['answer']} / {check['reason']}")
                st.write('형태소 및 품사:', check['tokens'])
        return

    st.write(f"문제 {st.session_state['quiz_index']}/{MAX_QUIZ}")

    if st.session_state['quiz_data'] is None:
        if st.button('문제 출제하기'):
            api_key = (os.getenv('OPENAI_API_KEY') or '').strip()
            model = (os.getenv('OPENAI_MODEL') or 'gpt-4.1-mini').strip()
            if not api_key:
                st.warning('.env 파일에 OPENAI_API_KEY를 설정하세요.')
            else:
                try:
                    client = make_client(api_key)
                    previous_questions = [row['question'] for row in st.session_state['log']]
                    with st.spinner('문제를 생성하고 있습니다...'):
                        quiz, in_tok, out_tok = ask_quiz(client, model, previous_questions)
                    st.session_state['input_tokens'] += in_tok
                    st.session_state['output_tokens'] += out_tok
                    valid, reason = validate_answer_word(quiz['answer'])
                    st.session_state['kiwi_checks'].append({
                        'number': st.session_state['quiz_index'],
                        'answer': quiz['answer'],
                        'valid': valid,
                        'reason': reason,
                        'tokens': [(token.form, token.tag) for token in kiwi.tokenize(quiz['answer'])]
                    })
                    if not valid:
                        raise ValueError(f"Kiwi 검사 실패: {quiz['answer']} / {reason}")
                    if normalize_answer(quiz['question']) in {
                        normalize_answer(q) for q in previous_questions
                    }:
                        raise ValueError('이전 문제와 중복되었습니다. 다시 출제해 주세요.')
                    st.session_state['quiz_data'] = quiz
                    st.session_state['question'] = quiz['question']
                    st.rerun()
                except (OpenAIError, ValueError, KeyError, TypeError, json.JSONDecodeError, OSError) as exc:
                    st.error(f'문제 출제 실패: {exc}')
        return

    quiz = st.session_state['quiz_data']
    st.subheader(st.session_state['question'])

    if st.session_state['answered']:
        if st.session_state['log'][-1]['correct']:
            st.success(st.session_state['result'])
        else:
            st.warning(st.session_state['result'])
        st.write('정답:', quiz['answer'])
        st.write('해설:', quiz['explanation'])
        with st.expander('Kiwi 정답 분석 결과'):
            check = st.session_state['kiwi_checks'][-1]
            st.write('검사 결과:', check['reason'])
            st.write('형태소 및 품사:', check['tokens'])
            st.caption('Kiwi 검사는 정답 형식과 형태소만 확인합니다. 아재개그의 타당성을 보장하지 않습니다.')
        label = '최종 결과 보기' if st.session_state['quiz_index'] == MAX_QUIZ else '다음 문제'
        if st.button(label):
            next_quiz()
            st.rerun()
    else:
        remaining = MAX_SUBMIT - st.session_state['attempts']
        st.write(f'남은 기회: {remaining}회')

        if st.button('힌트 보기', disabled=st.session_state['hint_used']):
            st.session_state['hint_used'] = True
            st.rerun()
        if st.session_state['hint_used']:
            st.info(f"힌트: {quiz['hint']} (정답 시 5점 감점)")

        with st.form(key=f"answer_form_{st.session_state['quiz_index']}"):
            answer = st.text_input(
                '정답 입력',
                key=f"answer_input_{st.session_state['quiz_index']}_{st.session_state['attempts']}"
            )
            submitted = st.form_submit_button('정답 제출')
        if submitted:
            if not answer.strip():
                st.warning('정답을 입력하세요.')
            else:
                correct, message = answer_quiz(answer)
                st.session_state['result'] = message
                st.rerun()

        if st.session_state['result']:
            st.warning(st.session_state['result'])

    st.caption(
        f"누적 토큰: 입력 {st.session_state['input_tokens']:,} / "
        f"출력 {st.session_state['output_tokens']:,}"
    )


if __name__ == '__main__':
    main()
