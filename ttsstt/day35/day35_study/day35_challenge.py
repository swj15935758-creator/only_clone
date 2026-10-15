# day35_challenge.py
# 주제:[Challenge: 철도역 음성 안내 신뢰성 리포트]
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

# 상황: 플랫폼 변경 안내를 STT로 기록하는 서비스를 검증합니다.
# 기본 전사 모델 사용법을 재활용하지 않고, 위험 키워드와 품질 지표를 결합합니다.

BASE = Path(__file__).resolve().parent

# 요구사항
# --- data ---
# 1. 정답·인식문·처리시간·재생시간으로 구성된 최소 4건 데이터를 준비하세요.
KEYWORDS = ("승강장", "출발", "변경")

SAMPLES = [
    ("열차 출발 시간은 오전 열 시입니다", # ref
     "열차 출발 시간은 오전 열 시입니다", # hyp
     2.1, # stt 처리시간
     6.0), # 음성파일 재생시간
    ("다음 열차는 삼 번 승강장에 도착합니다",
     "다음 열차는 삼 번에 도착합니다", 2.4, 7.0),
    ("열차 출발 장소가 변경되었습니다",
     "열차 장소가 되었습니다", 2.9, 6.0),
    ("안전선 안쪽에서 기다려 주세요",
     "안전선 안쪽에서 기다려 주세요", 1.5, 5.0)]

#
# --- data 설명 ---
# (
#     "열차 출발 시간은 오전 열 시입니다",  # Reference: 정답 문장
#     "열차 출발 시간은 오전 열 시입니다",  # Hypothesis: STT 예측 문장
#     2.1,   # STT 처리시간(초)으로 추정
#     6.0    # 음성 파일 재생시간(초)으로 추정
# )
# 환경변수 예정
WER_WARNING = 0.2
CER_WARNING = 0.1
RTF_WARNING = 1.0

# 정규화
def normalize_text(text):
    text = unicodedata.normalize('NFC', text).lower()
    text = re.sub(r'[^가-힣a-z0-9\s]', r' ', text)
    return re.sub(r'\s+', ' ', text).strip()

# 2. WER·CER·RTF를 계산하고 지표별 경고 기준을 정의하세요.
# wer cer 계산
# 평가
def evaluate(reference, hypothesis):
    ref_n = normalize_text(reference)
    hyp_n = normalize_text(hypothesis)

    if not ref_n:
        raise ValueError('정답이 없어서 오류율을 평가할 수 없습니다')

    counts = process_words(ref_n, hyp_n)

    return {
        'wer': wer(ref_n, hyp_n),
        'cer': cer(ref_n, hyp_n),
        'S': counts.substitutions,
        'D': counts.deletions,
        'I': counts.insertions,
        'reference_norm': ref_n,
        'hypothesis_norm': hyp_n
    }

# rtf 계산
def sample_rtf(SAMPLES):
    results = []
    rtf = []

    for reference, hyp, latency, duration in SAMPLES:
        eval_result = evaluate(reference, hyp)

        if duration <= 0:
            raise ValueError('음성 길이는 0보다 커야 합니다')

        rtf.append(latency / duration)
        results.append(eval_result)

    return results, rtf

# 3. '승강장', '출발', '변경' 중 정답에 존재하지만 인식문에 없는 키워드를 찾으세요.
def find_keywords(SAMPLES):
    results = []

    for reference, hypothesis, latency, duration in SAMPLES:
        missing_keywords = []

        ref_n = normalize_text(reference)
        hyp_n = normalize_text(hypothesis)

        for keyword in KEYWORDS:
            if keyword in ref_n and keyword not in hyp_n:
                missing_keywords.append(keyword)

        results.append(missing_keywords)

    return results

# 4. 위험 키워드 누락 건에 대해 자동 배포 금지(검토 필요) 판정을 내리세요.
def check_warning(results, rtf, missing_results):
    for index in range(len(results)):
        results[index]['rtf'] = rtf[index]
        results[index]['missing_keywords'] = ', '.join(missing_results[index])

        results[index]['wer_warning'] = results[index]['wer'] >= WER_WARNING
        results[index]['cer_warning'] = results[index]['cer'] >= CER_WARNING
        results[index]['rtf_warning'] = results[index]['rtf'] >= RTF_WARNING

        if missing_results[index]:
            results[index]['auto_block'] = True
            results[index]['decision'] = '자동 배포 금지(검토 필요)'

        elif (results[index]['wer_warning'] or results[index]['cer_warning'] or results[index]['rtf_warning']):
            results[index]['auto_block'] = False
            results[index]['decision'] = '지표 경고(검토 권장)'

        else:
            results[index]['auto_block'] = False
            results[index]['decision'] = '설정 기준 통과'

    return results

# 5. 행별 결과와 전체 요약을 CSV로 저장하세요.
def save_df(df, summary_df):
    output_path = BASE / 'challenge.csv'
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    pp(f'CSV 저장 경로: {output_path}')

    summary_path = BASE / 'challenge_summary.csv'
    summary_df.to_csv(summary_path, index=False, encoding='utf-8-sig')
    pp(f'전체 요약 CSV 저장 경로: {summary_path}')


def main():
    results, rtf = sample_rtf(SAMPLES)
    missing_results = find_keywords(SAMPLES)

    results = check_warning(results, rtf, missing_results)

    df = pd.DataFrame(results)

    summary_df = pd.DataFrame([{
        'total_samples': len(df),
        'wer_mean': df['wer'].mean(),
        'cer_mean': df['cer'].mean(),
        'rtf_mean': df['rtf'].mean(),
        'wer_warning_count': df['wer_warning'].sum(),
        'cer_warning_count': df['cer_warning'].sum(),
        'rtf_warning_count': df['rtf_warning'].sum(),
        'auto_block_count': df['auto_block'].sum()
    }])

    pp('안내문별 평가 결과')
    pp(df)

    pp('전체 요약')
    pp(summary_df)

    save_df(df, summary_df)



if __name__ == "__main__":
    main()