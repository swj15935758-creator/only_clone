
# day35_application.py
# 주제:[Application: 병원 안내방송 자동 자막 품질 비교]
#
# 상황: 병원 안내 문구를 자동 전사하는 시스템의 두 버전을 비교합니다.
# 실제 음성 파일이 없어도 제공 데이터로 모델별 비교가 가능합니다.
import re
from pathlib import Path
import unicodedata
from jiwer import wer, cer, process_words
from util.print_util import pp
import numpy as np
import pandas as pd

SAMPLES = [
    ("진료 예약은 일 층 접수처에서 확인하세요", # ref
     "진료 예약은 일 층 접수처에서 확인하세요", # A
     "진료 예약은 접수처에서 확인하세요",  # B
     7.0, 2.0, 3.0),  # 음성 전체 길이, A처리시간, B처리시간
    ("응급실 방문자는 안내 직원에게 문의하세요",
     "응급실 방문자는 안내 직원에게 문의하세요",
     "응급실 방문자는 안내 직원에게 문의", 6.0, 1.8, 2.8),
    ("검사 결과는 담당 의료진에게 확인하세요",
     "검사 결과는 담당 의료진에게 확인하세요",
     "검사 결과는 의료진에게 확인하세요", 6.5, 1.7, 2.7)]


BASE = Path(__file__).resolve().parent

# 요구사항
# 세 안내문과 모델 A/B의 인식문을 사용하세요. O
# 안내문별 WER·CER을 계산하고 모델별 평균을 표로 출력하세요.

def normalize_text(text):
    text = unicodedata.normalize('NFC', text).lower()
    text = re.sub(r'[^가-힣a-z0-9\s]', r' ', text)
    return re.sub(r'\s+', ' ', text).strip()

# 평가 함수
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

# 각 모델의 추론시간(가상 측정값 제공)을 사용해 RTF를 구하세요.

def sample_rtf(samples):
    results_a = []
    results_b = []
    rtf_a = []
    rtf_b = []

    for reference, hyp_a, hyp_b, duration, latency_a, latency_b in samples:
        eval_a = evaluate(reference, hyp_a)
        eval_b = evaluate(reference, hyp_b)

        if duration <= 0:
            raise ValueError('음성 길이는 0보다 커야 합니다')

        rtf_a.append(latency_a / duration)
        rtf_b.append(latency_b / duration)

        results_a.append(eval_a)
        results_b.append(eval_b)

    return results_a, results_b, rtf_a, rtf_b

# WER·CER·RTF 평균을 CSV로 저장하세요.
# csv 파일 평균 저장 함수
def save_wer_cer_rtf(rtf_a, rtf_b, results_a, results_b):
    df_a = pd.DataFrame(results_a)
    df_b = pd.DataFrame(results_b)

    rtf_a_mean = np.mean(rtf_a)
    rtf_b_mean = np.mean(rtf_b)

    wer_a_mean = df_a['wer'].mean()
    wer_b_mean = df_b['wer'].mean()

    cer_a_mean = df_a['cer'].mean()
    cer_b_mean = df_b['cer'].mean()

    df = pd.DataFrame([
        {
            'model': 'A',
            'WER_mean': wer_a_mean,
            'CER_mean': cer_a_mean,
            'RTF_mean': rtf_a_mean
        },
        {
            'model': 'B',
            'WER_mean': wer_b_mean,
            'CER_mean': cer_b_mean,
            'RTF_mean': rtf_b_mean
        }
    ])

    pp(df.round(3).to_string(index=False))

    output_path = BASE / 'wer_cer_rtf.csv'
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    pp(f'CSV 저장 경로: {output_path}')

# 의료용어 인식이 틀렸을 때의 위험과 자동화 한계를 설명하세요.

def main():
    results_a, results_b, rtf_a, rtf_b = sample_rtf(SAMPLES)

    detail_results = []

    for index in range(len(SAMPLES)):
        detail_results.append({
            'sample': index,
            'model': 'A',
            'WER': results_a[index]['wer'],
            'CER': results_a[index]['cer'],
            'RTF': rtf_a[index]
        })

        detail_results.append({
            'sample': index,
            'model': 'B',
            'WER': results_b[index]['wer'],
            'CER': results_b[index]['cer'],
            'RTF': rtf_b[index]
        })

    pp('안내문별 평가 결과')
    pp(pd.DataFrame(detail_results).round(3))

    pp('모델별 평균 평가 결과')
    save_wer_cer_rtf(rtf_a, rtf_b, results_a, results_b)

    pp('의료 안내 오류 위험: 층수나 담당 의료진 정보가 누락되면 환자가 잘못된 장소로 이동하거나 안내를 오해할 수 있습니다.')
    pp('자동화의 한계: 오류율이 낮아도 중요한 의료 정보가 틀릴 수 있으므로 핵심 안내문은 사람의 검토가 필요합니다.')


if __name__ == '__main__':
    main()
