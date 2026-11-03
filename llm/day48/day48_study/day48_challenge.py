# day48_challenge.py
# 주제:[민원 응답문 생성과 반복 제어 실험]
# 시나리오: 고객센터의 배송 지연 안내문을 생성하고 반복 제어가 미치는 영향을 정량적으로 관찰합니다.

import time
from pathlib import Path
import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from util.print_util import pp

# 요구사항
# 배송 지연, 환불 안내 등 고객 문의 3개를 영어로 준비합니다.
REQUESTS = [
    "A customer says their package arrived five days late.",
    "A customer requests a refund for a damaged product.",
    "A customer asks why shipment tracking has not updated.",
]

MODEL_ID = 'HuggingFaceTB/SmolLM2-135M-Instruct'
ROOT = Path(__file__).resolve().parent
OUT_FILE = ROOT / 'customer_support_results.csv'
MAX_NEW_TOKENS = 60 # 생성할 최대 토큰 수
SEED = 42

# 모델 가져오는 함수
def load_model():
    # GPU 사용가능하면 GPU에서 연산, 그렇지 않으면 cpu
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    pp(f'모델 로딩: {MODEL_ID}, 장치: {device}')
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID) # 학습된 토크나이저
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID) # 학습된 모델
    model.to(device) # 모델 가중치 계산을 gpu나 cpu 에서 수행
    model.eval() # 평가 모드로 변경
    return tokenizer, model, device

# 가져온 모델의 토크나이저 모델 디바이스를 state 번들에 저장
def ensure_model(state):
    if 'bundle' not in state:
        state['bundle'] = load_model()
    return state['bundle']

# 프롬프트에서 토큰을 생성하는 함수
def generate_text(tokenizer, model, device, prompts, params, seed=SEED):
    torch.manual_seed(seed)
    messages = [{'role': 'user', 'content': prompts}] # 사용자 프롬프트
    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors='pt'
    )
    inputs = {key: value.to(device) for key, value in inputs.items()}
    input_len = inputs['input_ids'].shape[1]

    if device == 'cuda':
        torch.cuda.synchronize()
    begin = time.perf_counter()

    with torch.inference_mode():
        output = model.generate(
            **inputs,
            pad_token_id=tokenizer.eos_token_id,
            **params
        )

    if device == 'cuda':
        torch.cuda.synchronize()
    seconds = time.perf_counter() - begin

    new_ids = output[0, input_len:]
    pp(f'생성 토큰 ID:{new_ids.tolist()}')
    pp('원본 출력', repr(
        tokenizer.decode(new_ids, skip_special_tokens=False)
    ))

    # 토큰 ID를 문자열로 디코딩
    answer = tokenizer.decode(new_ids, skip_special_tokens=True)
    tokens = len(new_ids)

    return {
        'answer': answer.strip(),
        'tokens': tokens,
        'seconds': round(seconds, 3)
    }

# 케이스 변환 함수
def run_case(state, name, request, params):
    tokenizer, model, device = ensure_model(state)
    options = {'max_new_tokens': MAX_NEW_TOKENS, **params}

    generation_prompt = (
        "Write a polite, concise customer support reply in English "
        "to this customer message:\n"
        f"{request}"
    )
    result = generate_text(
        tokenizer, model, device, generation_prompt, options
    )

    words = result['answer'].split()
    duplicate_rate = (
        (len(words) - len(set(words))) / len(words)
        if words else 0.0
    )

    record = {
        'setting': name,
        'request': request,
        'repetition_penalty': params['repetition_penalty'],
        'duplicate_rate': round(duplicate_rate, 3),
        **result
    }
    state['records'].append(record)

    pp(f"[{name}] {result['answer']}")
    pp(f"생성토큰: {result['tokens']}개")
    pp(f"생성시간: {result['seconds']}초")
    pp(f"단어 중복률: {duplicate_rate:.3f}")

# csv에 출력문을 저장합니다.
def save_csv(state):
    frame = pd.DataFrame(state['records'])
    frame.to_csv(OUT_FILE, index=False, encoding='utf-8-sig')
    pp('CSV 저장:', OUT_FILE)

# repetition_penalty를 1.0, 1.1, 1.3으로 바꿔 총 9건을 생성합니다.
repetition_penalty_list = [1.0, 1.1, 1.3]

def repetition_penalty(state):
    common = {'do_sample': True,'temperature': 0.8,'top_k': 50,'top_p': 1.0}

    for request_number, request in enumerate(REQUESTS, start=1):
        for value in repetition_penalty_list:
            run_case(state,f'request_{request_number}_penalty_{value}',request,{**common, 'repetition_penalty': value})

# 신규 토큰 수, 생성시간, 공백 구분 단어 기준 중복률을 계산합니다.
def main():
    state = {'records': [],}
    repetition_penalty(state)
    save_csv(state)

if __name__ == '__main__':
    main()

# customer_support_results.csv 파일로 모든 실험 결과를 저장합니다.