# day54_application.py
# 가상 교육 설문 6개를 실제 LLM으로 분석

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pe.day54.day54_ex import call_llm, parse_json, save_json
from util.print_util import pp, up

ROOT = Path(__file__).resolve().parent

FEEDBACK = [
    "실습이 실제 업무 사례라 좋았습니다.",
    "API 키 설정 방법을 자세히 알려주면 좋겠습니다.",
    "회의록 자동 정리는 바로 써볼 수 있을 것 같습니다.",
    "개념 설명에 비해 직접 따라 할 시간이 부족했습니다.",
    "매출 분석 과정에서 숫자 검증이 도움이 됐습니다.",
    "실습 후 결과를 비교하는 시간이 더 필요합니다.",
]

# 설문 원문을 근거로 개선 제안을 생성하는 함수
# client : API 클라이언트
# model : 사용할 텍스트 모델 ID
# feedback : 설문 문자열의 목록
# 반환값 : positive/issues/actions/evidence가 있는 dict
def summarize_feedback(client, model, feedback):
    instructions = (
        "교육 운영 분석 담당자. 제공된 설문만 근거로 JSON 객체 하나 출력. "
        "키는 positive, issues, actions, evidence. 값은 모두 문자열 목록. "
        "의견의 수를 과장하거나 존재하지 않는 피드백을 만들지 말 것. "
        "actions는 구체적인 교육 운영 개선안 3개 이내."
    )
    text = "\n".join(f"{i}. {v}" for i, v in enumerate(feedback, 1))
    raw, tokens, seconds = call_llm(client, model, instructions, text)
    pp("호출 사용량:", tokens, "소요(초):", seconds)
    return parse_json(raw)

def main():

    load_dotenv(ROOT / ".env")

    key = os.getenv("OPENAI_API_KEY", "").strip()

    if not key or key.startswith("sk-your-own"):
        raise SystemExit(".env 파일에 개인 API 키를 입력해야 함")

    client = OpenAI(api_key=key, timeout=45.0, max_retries=1)

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    data = summarize_feedback(client, model, FEEDBACK)

    save_json(ROOT / "output" / "application_feedback.json", data)

    pp("문항:", len(FEEDBACK), "개, JSON 키:", sorted(data))
    pp("근거 목록을 원문과 대조하고 교육 담당자가 승인해야 함")

if __name__ == "__main__":
    main()

up(5)









