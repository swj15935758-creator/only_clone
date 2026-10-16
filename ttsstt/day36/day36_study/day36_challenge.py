# day36_challenge.py
# [Challenge] 박물관 다국어 오디오 가이드 실험

import asyncio # 비동기 IO
import csv
import time
from pathlib import Path
import edge_tts # TTS online 모델
import pandas as pd
from mutagen import File as AudioFile # 파일의 메타데이터
from util.print_util import pp
OUT = Path(__file__).resolve().parent / 'out'

TEXTS = {
    "ko": ("우리 박물관의 역사 전시관에 오신 것을 환영합니다.",
           ["ko-KR-SunHiNeural", "ko-KR-InJoonNeural"]),
    "en": ("Welcome to the history gallery of our museum.",
           ["en-US-AriaNeural", "en-US-GuyNeural"]),
} # text voice1, voice2

# 폴더 생성
def mk_dir(path):
    path.mkdir(parents=True, exist_ok=True)

# 요구: 각 MP3로 저장하고 길이(초), 용량(bytes)을 info 등 정리 application이랑 바뀐 부분 voice의 디폴트값 없음
async def synthesize(text,filename,voice,rate='+0%',pitch='+0Hz'):
    target = OUT / filename
    # 음성 합성 객체
    tts = edge_tts.Communicate(text,voice=voice,rate=rate,pitch=pitch)

    start = time.perf_counter()
    await tts.save(str(target))
    end = time.perf_counter()
    elapsed = end - start

    audio = AudioFile(str(target)) # 메타데이터 조회

    # 오디오x or info 속성 x
    if audio is None or not hasattr(audio,'info'):
        raise ValueError(f'오디오 메타 데이터 분석 실패{target}')

    # 음성길이
    secs = round(audio.info.length,3)

    return {
        'filename': filename,
        'text': text,
        'voice': voice,
        'rate': rate,
        'pitch': pitch,
        'duration_sec' : secs,
        'size_bytes' : target.stat().st_size,
        'elapsed' : elapsed,
        'rtf': round(elapsed/secs,3) if secs else None
    }

# 성공 여부 확인 함수  rows 반환 합성 결과 수집
async def is_success(cases):
    is_pass = ''
    rows = []

    for filename, text, voice, rate, pitch in cases:
        try:
            row = await synthesize(text,filename,voice=voice,rate=rate,pitch=pitch)
            rows.append(row)
            is_pass = f'완료 : {filename} / {row["duration_sec"]}초'
        except Exception as e:
            is_pass = f'실패:{filename}:{type(e).__name__}:{e}'

        pp(is_pass)

    return rows

# 인덱스별 분리 하면서 case 파일명 voice준비 수정부분
def split_voices(cases):
    cases = [
        (f'tts_{voice}.mp3',text, voice,'+0%','+0Hz')
        for lang , (text, voices) in cases.items()
        for voice in voices
    ]
    return cases

# 빈 설문 CSV 만드는 함수 : 평가자가 실제 음성을 듣고 점수를 비교함
def mk_eval_csv(rows):
    with (OUT/'listening_scores.csv').open('w', newline='',encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['clip_id','evaluator','clarity','naturalness','comment'])
        for row in rows:
            writer.writerow([row['filename'],"","","",""])

# 결과를 CSV 파일로 저장 basic 이랑 바뀐부분 (수정 필요)
def summary_table(rows): # (3) 저장 확인
    if not rows:
        pp('저장할 음성 데이터가 없습니다.')
        return
    df = pd.DataFrame(rows)
    summary = df[['filename', 'voice', 'duration_sec', 'size_bytes', 'elapsed', 'rtf']]
    summary.to_csv(OUT / 'library_tts_summary_challenge.csv', index=False, encoding='utf-8-sig')
    pp(summary)
    pp(f'CSV 저장 완료: {OUT / "library_tts_summary_challenge.csv"}')

# case 추가 부분 (수정 필요)
def change_cases(cases):
    changed_cases = []

    for filename, text, voice, rate, pitch in cases:
        changed_cases += [
            (f'{Path(filename).stem}_pitch0.mp3', text, voice, rate, '+0Hz'),
            (f'{Path(filename).stem}_pitch15.mp3', text, voice, rate, '+15Hz')
        ]

    return changed_cases

async def main():
    mk_dir(OUT)
    cases = split_voices(TEXTS)
    changed_cases = change_cases(cases) # basic 에서 추가된 부분
    rows = await is_success(changed_cases)
    summary_table(rows)
    mk_eval_csv(rows)

if __name__ == '__main__':
    asyncio.run(main())
# 주제: 한국어·영어 박물관 소개 문장 및 음색/피치를 비교합니다.
# 조건: 한국어와 영어 안내 문장 각 1개, 2개 음색과 2개 피치 조합으로 합성합니다.
# 요구: 언어별 음색 2개×피치 2개 = 총 8개 MP3를 생성합니다.
# 평가: 평가자·명료도·자연스러움(1~5) CSV 서식 생성, 유효 응답 평균 집계.
# 조건: 음색은 서비스 제공 사전 등록 음색만 사용하고 개인화 복제는 수행하지 않습니다.

