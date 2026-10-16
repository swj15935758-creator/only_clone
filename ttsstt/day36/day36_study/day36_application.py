# day36_application.py
# [Application] 지하철 환승 안내 방송 A/B 테스트
# 주제: 환승 안내 문장을 기본/느리게/빠르게 3가지 속도로 합성합니다.
import asyncio # 비동기 IO
import csv
import time
from pathlib import Path
import edge_tts # TTS online 모델
import pandas as pd
from mutagen import File as AudioFile # 파일의 메타데이터
from util.print_util import pp

MESSAGES = [
    "이번 역은 시청역입니다. 이호선으로 갈아타실 수 있습니다.",
    "열차에서 내리실 때 발 빠짐에 주의해 주세요.",
]
# 환경변수 예정인 것[
# 보이스 설정 남자의 목소리
VOICE = 'ko-KR-InJoonNeural'
# 출력 파일 경로
OUT = Path(__file__).resolve().parent / 'out'
# ]

# 요구: 각 MP3로 저장하고 길이(초), 용량(bytes)을 info 등 정리
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

# case 추가 부분
def change_cases(cases): #  basic 이랑 바뀐부분
    changed_cases = []

    for filename,text,voice,rate,pitch in cases:
        changed_cases += [
            (f'{Path(filename).stem}_SLOW.mp3', text, voice, '-15%', '+0Hz'),
            (f'{Path(filename).stem}_base.mp3', text, voice, '+0%', '+0Hz'),
            (f'{Path(filename).stem}_fast.mp3', text, voice, '+15%', '+0Hz'),
        ]

    return changed_cases

# 인덱스별 분리 cases 파일명 준비
def split_voices(cases):
    cases = [
        (f'tts_{i:02}.mp3',text, VOICE,'+0%','+0Hz')
        for i, text in enumerate(cases, start=1)
    ]
    return cases

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

# 폴더 생성
def mk_dir(path):
    path.mkdir(parents=True, exist_ok=True)

# 결과를 CSV 파일로 저장 basic 이랑 바뀐부분
def summary_table(rows): # (3) 저장 확인
    if not rows:
        pp('저장할 음성 데이터가 없습니다.')
        return
    df = pd.DataFrame(rows)
    summary = df[['filename', 'rate', 'duration_sec', 'size_bytes', 'elapsed', 'rtf']]
    summary.to_csv(OUT / 'library_tts_summary_application.csv', index=False, encoding='utf-8-sig')
    pp(summary)
    pp(f'CSV 저장 완료: {OUT / "library_tts_summary_application.csv"}')

# 조건: 안내 문장 2개를 준비하고 각 문장마다 속도를 -15%, +0%, +15%로 비교합니다.
# 요구: 각 합성 결과 6개 파일을 저장하고 길이와 처리시간, RTF를 CSV로 정리합니다.
# 분석: 같은 문장 내에서 가장 긴 오디오와 가장 짧은 오디오를 비교합니다.

async def main():
    mk_dir(OUT)
    cases = split_voices(MESSAGES)
    changed_cases = change_cases(cases) # basic 에서 추가된 부분
    rows = await is_success(changed_cases)
    summary_table(rows)

if __name__ == '__main__':
    asyncio.run(main())

