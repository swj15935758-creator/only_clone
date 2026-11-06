# day51_prac1.py - GPT와 함께하는 끝말잇기

import os
import re
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

# 소스 파일과 같은 폴더의 .env에서 API 키와 모델을 읽음
load_dotenv(Path(__file__).resolve().parent / ".env")
API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()
MAX_TURNS = 5  # 사용자 단어 5개를 제출하면 게임 종료

# 사용자 또는 GPT 단어가 게임 규칙에 맞는지 검사하는 함수
# word : 검사할 단어
# last_word : 직전 단어, 첫 턴에서는 빈 문자열
# used_words : 이전에 사용한 단어 목록
# 반환값 : (정상 여부, 안내 메시지)
def validate_word(word, last_word, used_words):
    if not re.fullmatch(r"[가-힣]{2,5}", word):
        return False, "한글 2~5글자로 입력하세요."
    if word in used_words:
        return False, "이미 사용한 단어입니다."
    if last_word and word[0] != last_word[-1]:
        return False, f"'{last_word[-1]}'(으)로 시작해야 합니다."
    return True, "정상 단어"

# GPT에게 마지막 글자로 시작하는 다음 단어를 요청하는 함수
# client : OpenAI API 클라이언트
# last_word : 사용자가 제출한 직전 단어
# used_words : 중복 방지를 위한 전체 단어 목록
# 반환값 : Python 규칙 검사를 통과한 GPT 단어
# JSON 출력은 단어의 사전 등재 여부를 보장하지 않음
def ask_gpt(client, last_word, used_words):
    rules = (
        "한국어 끝말잇기 상대입니다. 한글 2~5글자 단어 하나만 생성하세요. "
        "직전 단어의 끝 글자로 시작하고 사용한 단어를 반복하지 마세요. "
        "두음법칙은 적용하지 않습니다."
    )
    for attempt in range(2):  # GPT의 잘못된 단어는 최대 1회 재요청
        response = client.responses.create(
            model=MODEL,
            instructions=rules,
            input=(f"직전 단어: {last_word}\n사용 목록: "
                   f"{', '.join(used_words)}\n시도: {attempt + 1}"),
            text={"format": {"type": "json_schema", "name": "word_reply",
                             "strict": True, "schema": {
                                 "type": "object",
                                 "properties": {"word": {"type": "string"}},
                                 "required": ["word"],
                                 "additionalProperties": False}}},
            max_output_tokens=100,
            store=False,
        )
        import json  # 문자열 JSON을 딕셔너리로 변환하기 위한 표준 라이브러리
        word = json.loads(response.output_text)["word"].strip()
        valid, _ = validate_word(word, last_word, used_words)
        if valid:
            return word
    raise ValueError("GPT가 두 번 모두 규칙에 맞는 단어를 만들지 못했습니다.")

# Streamlit이 화면을 다시 그려도 게임 기록을 유지하는 함수
# 반환값 : 없음, st.session_state 내부 키를 초기화함
def init_state():
    if "chain" not in st.session_state:
        st.session_state.chain = []
        st.session_state.turns = 0
        st.session_state.score = 0

# 게임을 다시 시작하는 함수
# 반환값 : 없음
def reset_game():
    st.session_state.chain = []
    st.session_state.turns = 0
    st.session_state.score = 0

# Streamlit 화면 구성 및 게임 진행 함수
# 반환값 : 없음
def main():
    st.set_page_config(page_title="LLM 끝말잇기")
    init_state()
    st.title("LLM 끝말잇기 게임")
    st.caption("사용자 선공 · 한글 2~5글자 · 두음법칙/사전 검사는 제외")
    st.button("새 게임", on_click=reset_game)
    st.metric("점수", f"{st.session_state.score}점")
    st.progress(st.session_state.turns / MAX_TURNS)
    st.write(f"진행: {st.session_state.turns}/{MAX_TURNS}턴")
    chain = st.session_state.chain
    st.write("사용한 단어:", " → ".join(chain) if chain else "아직 없음")
    if st.session_state.turns >= MAX_TURNS:
        st.success(f"게임 종료! 최종 점수: {st.session_state.score}점")
        return
    if not API_KEY:
        st.error("같은 폴더의 .env에 OPENAI_API_KEY를 설정하세요.")
        return
    if not MODEL:
        st.error("OPENAI_MODEL을 설정하세요.")
        return
    last_word = chain[-1] if chain else ""
    st.info(f"{'첫 단어를 입력하세요.' if not chain else '시작 글자: ' + last_word[-1]}")
    with st.form("word_form", clear_on_submit=True):
        typed = st.text_input("내 단어", max_chars=5)
        submitted = st.form_submit_button("제출하고 GPT와 대결")
    if submitted:
        word = typed.strip()
        valid, reason = validate_word(word, last_word, chain)
        if not valid:
            st.warning(reason)
            return
        # 마지막 사용자 턴에서는 GPT 응답이 필요하지 않음
        if st.session_state.turns + 1 == MAX_TURNS:
            chain.append(word)
        else:
            try:
                with st.spinner("GPT가 단어를 생각하는 중..."):
                    reply = ask_gpt(OpenAI(api_key=API_KEY), word,
                                    chain + [word])
            except (OpenAIError, ValueError, KeyError, OSError) as exc:
                st.error(f"GPT 응답 실패: {exc} (점수는 변하지 않음)")
                return
            chain.extend([word, reply])  # 두 단어 모두 성공했을 때만 기록
        st.session_state.turns += 1
        st.session_state.score += 10
        st.rerun()

if __name__ == "__main__":
    main()
