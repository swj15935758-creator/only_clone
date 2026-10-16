# challenge.pt
# 강사님 코드
import re
from pathlib import Path
import unicodedata
from jiwer import wer, cer, process_words
from util.print_util import pp
import numpy as np
import pandas as pd

KEYWORDS = ("승강장", "출발", "변경")
SAMPLES = [
    ("열차 출발 시간은 오전 열 시입니다",
     "열차 출발 시간은 오전 열 시입니다", 2.1, 6.0),
    ("다음 열차는 삼 번 승강장에 도착합니다",
     "다음 열차는 삼 번에 도착합니다", 2.4, 7.0),
    ("열차 출발 장소가 변경되었습니다",
     "열차 장소가 되었습니다", 2.9, 6.0),
    ("안전선 안쪽에서 기다려 주세요",
     "안전선 안쪽에서 기다려 주세요", 1.5, 5.0)]

def normalize_text(text):
    text = unicodedata.normalize('NFC', text).lower()
    text = re.sub(r'[^가-힣a-z0-9\s]', r' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def main():

    records = []

    for i, (reference, hypothesis, latency, duration)\
            in enumerate(SAMPLES, 1):
        ref_n , hyp_n = normalize_text(reference), normalize_text(hypothesis)
        word_rate, char_rate = wer(ref_n, hyp_n), cer(ref_n, hyp_n)
        rtf = latency / duration
        # 정답에는 있지만 인식에는 없는 키워드 리스트
        missing = [k for k in KEYWORDS if k in ref_n and k not in hyp_n]

        review = bool(missing) or word_rate > 0.2 or rtf > 1.0

        records.append({
            '번호':i,
            '정답':reference,
            '전사':hypothesis,
            'wer':word_rate,
            'cer':char_rate,
            'rtf':rtf,
            '누락키워드':','.join(missing),
            '판정': '검토 필요' if review else '자동 통과'
        })

    df = pd.DataFrame(records)
    summary = pd.DataFrame([{
        '전체':len(df),
        '검토필요':(df['판정']=='검토 필요').sum(),
        '평균wer': df['wer'].mean(),
        '평균cer': df['cer'].mean(),
        '평균rtf': df['rtf'].mean(),
    }])

    base = Path(__file__).resolve().parent

    df.to_csv(base / 'railway_report.csv', index=False, encoding='utf-8-sig')

    summary.to_csv(base / 'railway_summary.csv', index=False, encoding='utf-8-sig')

    pp(df.to_string(index=False))
    pp(summary.to_string(index=False))
    pp('위험한 자동 안내의 실제 개시에는 반드시 인적 검수가 필요합니다.')


if __name__ == '__main__':
    main()