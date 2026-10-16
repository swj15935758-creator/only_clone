# day36_ex1.py
#python -m pip install edge-tts mutagen
# 주제: 한국어 TTS 합성 및 청취 품질 평가

# Alt + F12 > pip install edge-tts, mutagen

import asyncio # 비동기 IO
import csv
import time
from pathlib import Path
import edge_tts # TTS online 모델
import pandas as pd
from mutagen import File as AudioFile # 파일의 메타데이터
from util.print_util import pp

# 출력 파일 경로
OUT = Path(__file__).resolve().parent /'outputs'

# edge-tts 에서 제공하는 voice id
VOICE = 'ko-KR-SunHiNeural'
ALT_VOICE = 'ko-KR-InJoonNeural'

# TTS 에 사용할 문장들
SAMPLES = [
    '안녕하세요. 접니다. 저라구요.',
    '오늘의 분석 결과는 나야 들기들',
    '잠시 후 다시 돌아오겠습니다.'
]

# 문장을 지정한 음색/ 속도 / 피치로 MP3에 저장하는 함수 synthesize 합성이라는뜻
async def synthesize(text,filename,voice=VOICE,rate='+0%',pitch='+0Hz'):
    target = OUT / filename

    # 음성 합성 객체
    tts = edge_tts.Communicate(text,voice=voice,rate=rate,pitch=pitch)

    start = time.perf_counter() # 시작시간
    await tts.save(str(target)) # 합성 결과를 MP3 저장
    end = time.perf_counter()  # 종료 시간
    elapsed = end - start # 소요시간

    audio = AudioFile(str(target)) # MP3를 읽어서 메타데이터 조회

    # audio가 없거나 info라는 속성이 없다면
    if audio is None or not hasattr(audio,'info'):
        raise ValueError(f'오디오 메타데이터 분석 실패{target}')

    seconds = round(audio.info.length, 3) # 음성 재생 길이(초)

    return {
        'file': filename, # 파일명
        'text': text, # 변환할 텍스트
        'voice': voice, # voice id
        'rate': rate, # 속도
        'pitch': pitch, # 높낮이
        'duration_sec': seconds, # 재생시간
        'size_bytes': target.stat().st_size, # 파일의 바이트 수
        'elapsed_sec': round(elapsed,3), # 처리 소요시간
        'rtf': round(elapsed / seconds,3)if seconds else None # RTF
    }

async def main():

    OUT.mkdir(parents=True, exist_ok=True)

    cases = [
        (f'tts_{i:02}.mp3',text, VOICE,'+0%','+0Hz')
        for i, text in enumerate(SAMPLES, start=1)
    ]

    base = '분석 결과를 확인해보세요.'

    cases += [
        ('cmp_base.mp3',base,VOICE,'+0%','+0Hz'), # 기본
        ('cmp_punct.mp3','분석 결과를 확인해 보세요.!',VOICE,'+0%','+0Hz'), # txt 교체
        ('cmp_SLOW.mp3',base,VOICE,'-20%','+0Hz'), # 속도 -20%
        ('cmp_fast.mp3',base,VOICE,'+20%','+0Hz'), # 속도 +20%
        ('cmp_pitch.mp3',base,VOICE,'+0%','+20Hz'), # 피치 +20Hz
        ('cmp_voice.mp3',base,ALT_VOICE,'+0%','+0Hz') # voice id 교체
    ]

    rows = []

    for filename, text, voice, rate, pitch in cases:
        try:
            row = await synthesize(text,filename,voice=voice,rate=rate,pitch=pitch)
            rows.append(row)
            pp(f'완료 : {filename} / {row["duration_sec"]}초')
        except Exception as e:
            pp(f'실패:{filename}:{type(e).__name__}:{e}')

    # 빈 설문 CSV : 평가자가 실제 음성을 듣고 점수를 깅비함
    with (OUT/'listening_scores.csv').open('w', newline='',encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['clip_id','evaluator','clarity','naturalness','comment'])
        for row in rows:
            writer.writerow([row['file'],"","","",""])
    pp('생성 완료: tts_metadata.csv, listening_scores.csv')
    pp('평가표를 작성한 뒤 day36_ex2.py를 실행하세요.')

if __name__ == '__main__':
    asyncio.run(main())


























































