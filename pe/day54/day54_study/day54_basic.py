# day54_basic.py
# 예약 변경 문의를 실제 OpenAI API로 구조화

import os
import time
import traceback
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pe.day54.day54_ex import parse_json, save_json
from util.print_util import pp, up

ROOT = Path(__file__).resolve().parent

QUESTIONS = [
    "문화센터 강좌 날짜를 다른 날로 옮길 수 있을까요?",
    "체육관 예약을 오늘 취소하면 환불되는지 알고 싶습니다.",
    "예약 시간에 시설 정전이 발생했습니다. 지금 확인해 주세요.",
]

RESERVATION_SCHEMA = {
    "type": "object",
    "properties": {
        "request_type": {
            "type": "string",
            "enum": ["변경", "취소", "긴급", "기타"]
        },
        "urgency": {
            "type": "string",
            "enum": ["high", "normal"]
        },
        "answer": {"type": "string"},
        "human_check": {"type": "boolean"}
    },
    "required": ["request_type", "urgency", "answer", "human_check"],
    "additionalProperties": False
}

# 문의의 의도와 응답 초안을 만드는 함수
# client : OpenAI 클라이언트 객체
# model : 사용 가능한 OpenAI 모델 이름
# question : 하나의 가상 예약 문의
# 반환값 : 구조화한 응답 dict
def handle_question(client, model, question):
    rules = (
        "공공시설 예약 문의 담당자입니다. 제공된 문의 내용만 근거로 답하세요. "
        "정전 등 시설 이용에 문제가 생긴 긴급 상황은 긴급/high로 분류하세요. "
        "answer는 정중한 한국어 답장 초안으로 작성하세요. "
        "확인하지 못한 환불 규정이나 예약 가능 여부를 단정하지 마세요. "
        "사람의 확인이 필요한 경우 human_check를 true로 설정하세요."
    )

    pp("문의:", question)

    started = time.perf_counter()
    response = client.responses.create(
        model=model,
        instructions=rules,
        input=question,
        text={
            "format": {
                "type": "json_schema",
                "name": "reservation_reply",
                "schema": RESERVATION_SCHEMA,
                "strict": True
            }
        },
        max_output_tokens=1600,
        store=False
    )
    seconds = round(time.perf_counter() - started, 2)

    if response.status != "completed":
        reason = getattr(response.incomplete_details, "reason", None)
        raise ValueError(
            f"응답이 완료되지 않았습니다: {response.status}, 사유: {reason}"
        )

    raw = response.output_text
    pp("모델 원본 응답:", repr(raw))

    if not raw:
        raise ValueError("모델의 텍스트 응답이 비어 있습니다.")

    result = parse_json(raw)

    if set(result) != set(RESERVATION_SCHEMA["required"]):
        raise ValueError("응답 필드 구성이 올바르지 않습니다.")
    if not isinstance(result["answer"], str) or not result["answer"].strip():
        raise ValueError("답장 초안이 비어 있습니다.")

    usage = response.usage
    tokens = {
        "input_tokens": getattr(usage, "input_tokens", None),
        "output_tokens": getattr(usage, "output_tokens", None)
    }
    pp("토큰/초:", tokens, seconds)
    time.sleep(3)
    return result

def main():
    load_dotenv(ROOT / ".env")

    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key or key.startswith("sk-your-own"):
        raise SystemExit(".env 파일에 API 키를 먼저 설정해야 함")

    client = OpenAI(api_key=key, timeout=45.0, max_retries=1)
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    answers = []
    failures = 0

    for question in QUESTIONS:
        try:
            answer = handle_question(client, model, question)
            answers.append({"question": question, "answer": answer})
        except Exception as exc:
            failures += 1
            pp("문의 처리 오류:", type(exc).__name__, str(exc))
            traceback.print_exc()

    save_json(ROOT / "output" / "basic_reservations.json", answers)
    pp("완료:", len(answers), "건 / 실패:", failures,
       "건. 실제 발송 전 사람 확인 필요")

if __name__ == "__main__":
    main()
    up(5)