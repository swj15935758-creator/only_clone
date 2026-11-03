# day48_application.py
# 주제:[여행 일정 안내문 생성 실험]
#
# 시나리오: 도시 여행 계획을 요청하는 문장을 생성하며, Top-k/Top-p 조합을 비교합니다.

import time
from pathlib import Path
import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from util.print_util import pp

MODEL_ID = 'HuggingFaceTB/SmolLM2-135M-Instruct'
ROOT = Path(__file__).resolve().parent
OUT_FILE = ROOT / 'travel_results.csv'
MAX_NEW_TOKENS = 60 # 생성할 최대 토큰 수

# 요구사항
# 한 도시의 1일 여행 소개문을 영어로 생성하도록 지시합니다.
prompt = ("Recommend a one-day walking itinerary in Kyoto "
              "in three concise English sentences.")
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
def run_case(state, name, params):
    tokenizer, model, device = ensure_model(state)
    options = {'max_new_tokens': MAX_NEW_TOKENS, **params}
    result = generate_text(tokenizer, model, device, prompt, options)
    record = {'setting': name, **result}
    state['records'] = [
        row for row in state['records'] if row['setting'] != name
    ]
    state['records'].append(record)
    pp(f"[{name}] {result['answer']}")
    pp(f"생성토큰: {result['tokens']}개")
    pp(f"생성시간: {result['seconds']}초")

# do_sample=True에서 top_k=10, top_k=50, top_p=0.75, top_p=0.95를 비교합니다.
def top_k10(state):
    pp('top_k=10')
    run_case(state, 'top_k_10',{
        'do_sample': True,'top_k':10,'top_p':1.0
    })

def top_k50(state):
    pp('top_k=50')
    run_case(state, 'top_k_50',{
        'do_sample': True,'top_k':50,'top_p':1.0
    })

# Top-p 실험에는 top_k=0을 설정하여 Top-k 필터를 해제합니다.
def top_p75(state):
    pp('top_p=0.75')
    run_case(state, 'top_p_75', {
        'do_sample': True, 'top_k': 0, 'top_p': 0.75
    })

def top_p95(state):
    pp('top_p=0.95')
    run_case(state, 'top_p_95', {
        'do_sample': True, 'top_k': 0, 'top_p': 0.95
    })

# 결과, 옵션, 생성시간을 travel_results.csv로 저장합니다.
def save_csv(state):
    frame = pd.DataFrame.from_dict(state['records'])
    frame.to_csv(OUT_FILE, index=False, encoding='utf-8-sig')
    pp('저장')

def main():
    state = {'records': []}
    top_k10(state)
    top_k50(state)
    top_p75(state)
    top_p95(state)
    save_csv(state)

# 과도하게 생성된 문장을 식별하고 사람이 직접 품질을 평가합니다.
if __name__ == '__main__':
    main()
