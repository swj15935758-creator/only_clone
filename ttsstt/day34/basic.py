# day34_basic.py
# 주제:
# day34_application.py
# 주제:
# Basic: 실제 매장·시장 현장음 품질 점검
# 업무 상황
# 서로 다른 장소에서 녹음된 현장음을 전달받았습니다.
# 파일별 음량과 녹음 조건을 비교하여 검토 대상 파일을 추려야 합니다.
#
# 실제 데이터
# store_audio/store_A.wav: 실제 시장 현장 녹음(12초)
# store_audio/store_B.wav: 실제 슈퍼마켓 계산대 녹음(13초)
# store_audio/store_C.wav: 실제 시장 현장 녹음의 다른 구간(15초)
#
# 요구사항
# 정확히 위 WAV 3개를 읽으세요. 없으면 누락 파일을 안내하세요.
# 파일명, 길이(초), 샘플링레이트, 채널 수를 조사하세요.
# 피크 진폭(peak)과 RMS 음량 지표를 구하세요.
# 피크 0.03 미만은 recheck, 나머지는 ok로 분류하세요.(0.03은 연습용 임계값이므로 실제 방송 적합성 판정은 아닙니다.)
# store_audio_check.csv로 결과를 저장하세요.
# 원본 WAV는 수정하지 마세요.
#
# 결과물
# store_audio_check.csv: 파일별 길이·샘플링레이트·채널·피크·RMS·상태
# 콘솔에 파일별 검사 결과 출력

import csv
from csv import DictWriter
from pathlib import Path
import numpy as np
import librosa
import soundfile as sf
import matplotlib.pyplot as plt
from util.print_util import pp, up

ROOT = Path(__file__).resolve().parent

SOURCES = {
    'store_audio' : ('store_A.wav', 'store_B.wav', 'store_C.wav')
}

REPORT = ROOT /  'reports'


# 정확히 위 WAV 3개를 읽으세요. 없으면 누락 파일을 안내하세요.
def find_wav():
    missing = []
    found = []

    for folder, names in SOURCES.items():
        for name in names:
            path = ROOT / folder / name
            if path.is_file():
                found.append((folder,path))
            else:
                missing.append(f'{folder}/{name}')
    if missing:
        pp('실제 녹음 파일이 준비되지 않았습니다.')
        for name in missing:
            pp('누락된 파일: ', name)
        return []

    return found
# 파일명, 길이(초), 샘플링레이트, 채널 수를 조사하세요.
# 피크 0.03 미만은 recheck, 나머지는 ok로 분류하세요.(0.03은 연습용 임계값이므로 실제 방송 적합성 판정은 아닙니다.)

def inspect(y, sr, path):
    if y.size == 0 or sr <= 0 or not np.isfinite(y).all():
        raise ValueError('비어 있거나 유효하지 않은 음성 데이터입니다.')

    # RMS와 Peak 계산을 위해 모노로 변환 (원본 y는 수정하지 않음)
    mono = librosa.to_mono(y) if y.ndim == 2 else y

    peak = float(np.max(np.abs(mono)))
    rms = float(np.sqrt(np.mean(mono ** 2)))

    return {
        'filename': path.name,
        'duration': round(librosa.get_duration(y=y, sr=sr), 3),
        'sample_rate': sr,
        'channels': 1 if y.ndim == 1 else y.shape[0],
        'peak': round(peak, 5),
        'rms': round(rms, 5),
        'status': 'recheck' if peak < 0.03 else 'ok'
    }


def main():
    found = find_wav()
    if not found:
        return

    REPORT.mkdir(exist_ok=True)

    fields = ['filename', 'duration', 'sample_rate', 'channels', 'peak', 'rms', 'status']
    report = REPORT / 'store_audio_check.csv'

    rows = []
    for group, path in found:
        # 원본 WAV 파일 읽기 (원본은 수정하지 않음)
        y, sr = librosa.load(path, sr=None, mono=False)

        # 파일 조사 및 지표 계산
        row = inspect(y, sr, path)
        rows.append(row)

        # 콘솔에 파일별 검사 결과 출력
        pp(row['filename'], row['status'], f"Peak: {row['peak']}", f"RMS: {row['rms']}")

    # CSV 파일 저장
    with report.open('w', encoding='utf-8-sig', newline='') as f:
        writer = DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    pp(f'CSV 보고서 저장 완료: {report}')
if __name__ == '__main__':
    main()
# store_audio_check.csv로 결과를 저장하세요.
# 원본 WAV는 수정하지 마세요.

