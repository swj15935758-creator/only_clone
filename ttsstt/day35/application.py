# application.py
# 강사님 코드

import re
import unicodedata
from pathlib import Path
import pandas as pd
from jiwer import cer,wer,process_words
from util.print_util import pp

SAMPLES = [
    ("진료 예약은 일 층 접수처에서 확인하세요",
     "진료 예약은 일 층 접수처에서 확인하세요",
     "진료 예약은 접수처에서 확인하세요", 7.0, 2.0, 3.0),
    ("응급실 방문자는 안내 직원에게 문의하세요",
     "응급실 방문자는 안내 직원에게 문의하세요",
     "응급실 방문자는 안내 직원에게 문의", 6.0, 1.8, 2.8),
    ("검사 결과는 담당 의료진에게 확인하세요",
     "검사 결과는 담당 의료진에게 확인하세요",
     "검사 결과는 의료진에게 확인하세요", 6.5, 1.7, 2.7)]

# 정규화 함수
def norm(value):
    value = unicodedata.normalize('NFC', value).lower()
    value = re.sub(r'[^가-힣a-z0-9\s]', 'r',value)
    return re.sub(r'\s+', ' ', value).strip()

def main():
    rows = []

    for i, (ref,a,b,duration, time_a, time_b) \
            in enumerate(SAMPLES, 1):
        for model, hyp, latency in [('A',a,time_a),('B',b,time_b)]:
            ref_n, hyp_n = norm(ref), norm(hyp)

            rows.append({
                '문장':i,
                '모델':model,
                'wer':wer(ref_n,hyp_n),
                'cer':cer(ref_n,hyp_n),
                'rtf': latency/duration
            })

    df = pd.DataFrame(rows)

    summary = df.groupby('모델', as_index=False)[['wer','cer','rtf']].mean()

    target = Path(__file__).resolve().parent / 'hospital_stt_summary.csv'

    summary.to_csv(target, index=False, encoding='utf-8-sig')

    pp(df.to_string(index=False))
    pp(summary.to_string(index=False))
    pp('의료 상황 낮은 오류율만으로 안정성을 보장할 수 없습니다')
    pp('개선: 핵심 용어 인적 검수, 불확실한 전사 표시 후 재 확인')
    pp(f'저장: {target}')

if __name__ == "__main__":
    main()