# day48_basic.py
# 주제:[상품 상세문구 생성 옵션 실험]

# 시나리오: 온라인 쇼핑몰의 상품 설명을 생성합니다.
import time
from pathlib import Path
import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from util.print_util import pp

# 요구사항
# 상품명과 특징(예: 휴대용 텀블러/가벼움·보온)을 영어 입력문으로 구성합니다.
prompt = ("Write two short promotional sentences about a travel mug "
          "that is light and keeps drinks warm. Use plain English.")

MODEL_ID = 'HuggingFaceTB/SmolLM2-135M-Instruct'
ROOT = Path(__file__).resolve().parent
OUT_FILE = ROOT / 'product_copy.csv'
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

# 같은 상품에 대해 Greedy와 Sampling 두 방식으로 문구를 생성합니다.
# Greedy로 생성 함수
def greedy_gen(state):
    run_case(state, 'greedy', {'do_sample': False})

# sampling으로 생성 함수
def sampling_gen(state):
    run_case(state, 'sampling', {'do_sample': True})

# 각 결과의 신규 토큰 수와 실행 시간을 화면에 표시합니다.
# product_copy.csv에 출력문을 저장합니다.
def save_csv(state):
    frame = pd.DataFrame(state['records'])
    frame.to_csv(OUT_FILE, index=False, encoding='utf-8-sig')
    pp('CSV 저장:', OUT_FILE)

def main():
    state = {'records': []}
    greedy_gen(state)
    sampling_gen(state)
    save_csv(state)

if __name__ == '__main__':
    main()