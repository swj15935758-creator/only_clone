# day35_ex.py
# 사전학습 STT 전사, WER, CER, 지연시간 평가

import csv
import re
import time
import unicodedata
import wave
from pathlib import Path
import pandas as pd
from jiwer import wer, cer, process_words
from faster_whisper import WhisperModel
from util.print_util import pp, up

BASE = Path(__file__).resolve().parent # 현재 파일의 디렉토리
AUDIO = BASE / 'audio' # 원본 오디오 파일 경로
REF_CSV = BASE / 'references.csv' # 정답파일 경로
OUT = BASE / 'results' / 'stt_results.csv' # 분석결과 저장 CSV 파일 경로

MODEL_NAME = 'tiny' # CPU 실행 가능한 다국어 STT 모델

# 두가지 실행 조건 : 조건명, beam_size, vad_filter
CONDITIONS = [
    ('baseline', 1, False),
    ('search_vad', 5, True)
]

# 같은 규칙으로 정답과 예측을 정규화하는 함수
def normalize_text(text):
    # NFC 정규화 후 소문자로 변환
    text = unicodedata.normalize('NFC', text).lower()
    text = re.sub(r'[^가-힣a-z0-9\s]', r' ', text)
    return re.sub(r'\s+', ' ', text).strip()

# CSV파일명을 기준으로 정답 문장을 가져오는 함수
def read_references(path):
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f)) # 각 행을 딕셔너리로 읽음
    # 행이 없거나 컬럼명이 다르다면
    if not rows or not {'file', 'reference'}.issubset(rows[0]):
        raise ValueError('references.csv에 file, reference 컬럼이 필요함')
    return rows

# 표준 PCM WAV에서 재생시간을 구하는 함수
def wav_duration(path):
    with wave.open(str(path), 'rb') as stream:
        frames = stream.getnframes() # 프레임 수
        sr = stream.getframerate() # 초당 프레임 수 (Hz)
        return frames / sr # 재생 시간

# 정규화 후 오류율과 단어 편집 연산 수를 구하는 함수
def evaluate(ref, hyp):
    ref_n = normalize_text(ref)
    hyp_n = normalize_text(hyp)
    if not ref_n:
        raise ValueError('정답이 빈 문장이라 오류율을 평가할 수 없습니다.')
    counts = process_words(ref_n, hyp_n) # 대체, 삭제, 삽입 획득
    return {
        'wer': wer(ref_n, hyp_n),
        'cer': cer(ref_n, hyp_n),
        'S': counts.substitutions,
        'D': counts.deletions,
        'I': counts.insertions,
        'reference_norm': ref_n,
        'hypothesis_norm': hyp_n
    }

# 전사 함수
def transcribe(model, path, beam_size, vad_filter):
    start = time.perf_counter() # 전사 시작 시간
    # 전사 후 segment들의 iterable과 부가 정보 획득
    segments, info = model.transcribe(
        str(path), # 파일경로 문자열
        language='ko', # 언어 설정
        beam_size=beam_size, # 확인 대상 개수
        vad_filter=vad_filter # 비발화 구간 필터링 여부
    )

    # 각 segment의 text들을 모아서 문장으로 생성
    text = ' '.join(s.text.strip() for s in segments).strip()
    end = time.perf_counter() # 전사 종료 시간
    elapsed = end - start # 전사 소요 시간

    return text, elapsed

def main():

    if not REF_CSV.exists():
        pp('references.csv 파일이 없습니다.')
        return

    # CSV파일내의 행들
    rows = read_references(REF_CSV)

    start_load = time.perf_counter() # 모델 로딩 시작 시간

    # 모델 생성
    model = WhisperModel(
        MODEL_NAME, # tiny
        device='cpu', # CPU 사용
        compute_type='int8' # 연산시 1바이트 정수로 변환 연산
    )

    end_load = time.perf_counter() # 모델 로딩 종료 시간

    elapsed_load = end_load - start_load # 모델 로딩 소요 시간
    pp(f'모델 로딩 소요 시간: {elapsed_load:.2f} 초')

    results = [] # 결과 저장 리스트

    for row in rows:

        path = AUDIO / Path(row['file']).name # CSV파일에서 읽은 WAV파일 경로

        if not path.is_file():
            pp(f'파일 없음: {path.name}')
            continue # 다음 행으로 이동

        try:

            duration = wav_duration(path) # 재생 시간

            if duration <= 0:
                pp(f'길이가 0인 파일: {path.name}')
                continue

            for label, beam, vad in CONDITIONS:
                hyp, latency = transcribe(model, path, beam, vad)
                metrics = evaluate(row['reference'], hyp)

                item = {
                    'file': path.name,
                    'condition': label,
                    'model': MODEL_NAME,
                    'beam_size': beam,
                    'vad_filter': vad,
                    'reference': row['reference'],
                    'hypothesis': hyp,
                    'audio_sec': round(duration, 3),
                    'latency_sec': round(latency, 3),
                    'rtf': round(latency / duration, 3),
                    **metrics
                }

                results.append(item)
                pp(
                    f"{path.name} [{label}], WER={metrics['wer']:.2%}"
                    f", CER={metrics['cer']:.2%}, Latency={latency:.2f}초"
                )

        except (ValueError, OSError, EOFError) as e:
            pp(f'입력/평가 오류: {path.name}: {e}')

    if not results:
        pp('유효한 WAV 데이터가 없어 결과를 저장하지 않습니다.')
        return

    OUT.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(results)
    df.to_csv(OUT, index=False, encoding='utf-8-sig')

    pp(df[['file', 'condition', 'wer', 'cer', 'latency_sec', 'rtf']])
    pp(f'저장 경로: {OUT}')

if __name__ == '__main__':
    main()

up(5)