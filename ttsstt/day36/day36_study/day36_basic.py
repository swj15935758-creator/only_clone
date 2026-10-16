# day36_basic.py
# [Basic] 도서관 안내 멘트 제작
#
# 주제: 도서관의 운영시간·열람실 이용 안내 3개 문장을 합성합니다.
#
# 조건: 본 실습에서 사용하지 않은 도서관 안내 문장 3개를 직접 구성합니다.
import asyncio # 비동기 IO
import csv
import time
from pathlib import Path
import edge_tts # TTS online 모델
import pandas as pd
from mutagen import File as AudioFile # 파일의 메타데이터
from util.print_util import pp

# 보이스 설정 남자의 목소리
VOICE = 'ko-KR-InJoonNeural'

# 출력 파일 경로
OUT = Path(__file__).resolve().parent / 'out'

MESSAGES = [
    "도서관은 오전 아홉 시부터 오후 여섯 시까지 운영합니다.",
    "열람실에서는 휴대전화를 진동으로 설정해 주세요.",
    "대출 도서는 반납함을 이용해 돌려주실 수 있습니다.",
]

# 요구: 각 MP3로 저장하고 길이(초), 용량(bytes)을 CSV로 정리합니다.
async def synthesize(text,filename,voice=VOICE,rate='+0%',pitch='+0Hz'):
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
# 폴더 생성
def mk_dir(path):
    path.mkdir(parents=True, exist_ok=True)

# 인덱스별 분리 (1번) cases 파일명 준비
def split_voices(cases):
    cases = [
        (f'tts_{i:02}.mp3',text, VOICE,'+0%','+0Hz')
        for i, text in enumerate(cases, start=1)
    ]
    return cases

# 성공 여부 확인 함수 (2) rows 반환 합성 결과 수집
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

# 결과를 CSV 파일로 저장
def summary_table(rows): # (3) 저장 확인
    if not rows:
        pp('저장할 음성 데이터가 없습니다.')
        return
    df = pd.DataFrame(rows)
    summary = df[['filename', 'duration_sec', 'size_bytes']]
    summary.to_csv(OUT / 'library_tts_summary.csv', index=False, encoding='utf-8-sig')
    pp(summary)
    pp(f'CSV 저장 완료: {OUT / "library_tts_summary.csv"}')

async def main():
    mk_dir(OUT)
    cases = split_voices(MESSAGES)
    rows = await is_success(cases)
    summary_table(rows)

if __name__ == '__main__':
    asyncio.run(main())

# 제약: 개인 식별 정보 및 실제 사용자 음성은 포함하지 않습니다.