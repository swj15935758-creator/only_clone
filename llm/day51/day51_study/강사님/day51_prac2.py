# day51_prac2.py - GPT가 출제하는 아재퀴즈 5문제

import json
import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

# .env에 OPENAI_API_KEY와 OPENAI_MODEL(선택)을 저장
load_dotenv(Path(__file__).resolve().parent / ".env")
API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()
MAX_QUIZZES = 5  # 한 게임에 5문제

# 공백과 영문 대소문자 차이를 없애 정답을 비교하기 위한 함수
# text : 비교할 답변
# 반환값 : 공백 제거 및 소문자 변환 문자열
def normalize(text):
    return "".join(text.lower().split())

# GPT에게 문제 1개와 정답·힌트·해설을 JSON으로 요청하는 함수
# client : OpenAI API 클라이언트
# 반환값 : question, answer, hint, explanation 키를 가진 딕셔너리
# 같은 뜻의 다른 정답은 자동 인정하지 않음
def request_quiz(client):
    fields = ["question", "answer", "hint", "explanation"]
    schema = {
        "type": "object",
        "properties": {name: {"type": "string"} for name in fields},
        "required": fields,
        "additionalProperties": False,
    }
    response = client.responses.create(
        model=MODEL,
        instructions=(
            "한국어 아재개그 문제를 하나 만드세요. 짧고 재미있으며 "
            "대표 정답이 하나인 말장난 문제로 만드세요. "
            "문제에 정답을 노출하지 마세요. "
            "question, answer, hint, explanation을 작성하세요."
        ),
        input="새로운 아재퀴즈 한 문제를 출제하세요.",
        text={"format": {"type": "json_schema", "name": "dad_quiz",
                         "strict": True, "schema": schema}},
        max_output_tokens=250,
        store=False,
    )
    quiz = json.loads(response.output_text)
    if not all(isinstance(quiz.get(name), str) and
               quiz[name].strip() for name in fields):
        raise ValueError("GPT가 문제의 필수 항목을 비워 반환했습니다.")
    return quiz

# 화면이 새로 그려져도 점수와 현재 문제를 유지하는 함수
# 반환값 : 없음
def init_state():
    if "quiz_number" not in st.session_state:
        reset_game()

# 모든 게임 데이터를 처음 상태로 되돌리는 함수
# 반환값 : 없음
def reset_game():
    st.session_state.quiz_number = 0
    st.session_state.quiz = None
    st.session_state.score = 0
    st.session_state.attempts = 0
    st.session_state.hint_used = False
    st.session_state.revealed = False
    st.session_state.results = []

# 현재 문제를 끝내고 결과를 저장하는 함수
# earned : 현재 문제에서 획득한 점수
# 반환값 : 없음
def finish_question(earned):
    st.session_state.score += earned
    st.session_state.revealed = True
    st.session_state.results.append({
        "question": st.session_state.quiz["question"],
        "answer": st.session_state.quiz["answer"],
        "score": earned,
    })

# Streamlit 화면 구성 및 게임 진행 함수
# 반환값 : 없음
def main():
    st.set_page_config(page_title="LLM 아재퀴즈")
    init_state()
    st.title("LLM 아재퀴즈 게임")
    st.caption("총 5문제 · 문제당 기회 2번 · 힌트 사용 시 5점 감점")
    st.button("새 게임", on_click=reset_game)
    st.metric("현재 점수", f"{st.session_state.score}점")
    if not API_KEY:
        st.error("같은 폴더의 .env에 OPENAI_API_KEY를 설정하세요.")
        return
    if not MODEL:
        st.error("OPENAI_MODEL을 설정하세요.")
        return
    if st.session_state.quiz_number >= MAX_QUIZZES:
        st.success(f"모든 문제 완료! 총 {st.session_state.score}점 / 100점")
        st.table(st.session_state.results)
        return
    st.write(f"문제 {st.session_state.quiz_number + 1}/{MAX_QUIZZES}")
    if st.session_state.quiz is None:
        if st.button("문제 출제하기"):
            try:
                with st.spinner("GPT가 문제를 만드는 중..."):
                    st.session_state.quiz = request_quiz(
                        OpenAI(api_key=API_KEY))
            except (OpenAIError, ValueError, KeyError, OSError) as exc:
                st.error(f"문제 생성 실패: {exc}")
            else:
                st.rerun()
        return
    quiz = st.session_state.quiz
    st.subheader(quiz["question"])
    if st.session_state.revealed:
        st.success(f"정답: {quiz['answer']}")
        st.write(f"해설: {quiz['explanation']}")
        if st.button("다음 문제"):
            st.session_state.quiz_number += 1
            st.session_state.quiz = None
            st.session_state.attempts = 0
            st.session_state.hint_used = False
            st.session_state.revealed = False
            st.rerun()
        return
    st.write(f"남은 기회: {2 - st.session_state.attempts}회")
    if st.button("힌트 보기", disabled=st.session_state.hint_used):
        st.session_state.hint_used = True
        st.rerun()
    if st.session_state.hint_used:
        st.info(f"힌트: {quiz['hint']}")
    with st.form("answer_form", clear_on_submit=True):
        user_answer = st.text_input("정답 입력")
        submitted = st.form_submit_button("정답 제출")
    if submitted:
        if not normalize(user_answer):
            st.warning("정답을 입력하세요. 기회는 차감되지 않습니다.")
            return
        st.session_state.attempts += 1
        if normalize(user_answer) == normalize(quiz["answer"]):
            base = 20 if st.session_state.attempts == 1 else 10
            earned = max(0, base - (5 if st.session_state.hint_used else 0))
            finish_question(earned)
            st.rerun()
        elif st.session_state.attempts >= 2:
            finish_question(0)
            st.rerun()
        else:
            st.warning("아쉽네요! 한 번 더 도전해 보세요.")

if __name__ == "__main__":
    main()
