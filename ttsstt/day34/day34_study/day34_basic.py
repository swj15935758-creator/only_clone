# day34_basic.py
# 주제:Basic: 실제 매장·시장 현장음 품질 점검
# 업무 상황
# 서로 다른 장소에서 녹음된 현장음을 전달받았습니다.
# 파일별 음량과 녹음 조건을 비교하여 검토 대상 파일을 추려야 합니다.
import csv
from pathlib import Path
import numpy as np
import librosa
import soundfile as sf
import matplotlib.pyplot as plt
from util.print_util import pp

# 실제 데이터
# store_audio/store_A.wav: 실제 시장 현장 녹음(12초)
# store_audio/store_B.wav: 실제 슈퍼마켓 계산대 녹음(13초)
# store_audio/store_C.wav: 실제 시장 현장 녹음의 다른 구간(15초)

ROOT = Path(__file__).resolve().parent

SOURCES = {
    'store_audio' : ('store_A.wav','store_B.wav','store_C.wav'),
}

LOAD = ROOT.parent # 가져올 파일이 있는 상위 폴더
SAVE = ROOT / 'save_audio' # 저장할 폴더 위치

# 요구사항
# 정확히 위 WAV 3개를 읽으세요. 없으면 누락 파일을 안내하세요.
def find_recordings():
    missing = [] # 없는 파일 이름
    found = [] # 찾은 파일 이름

    for folder, names in SOURCES.items():
        for name in names:
            path = LOAD / folder / name # 가져올 폴더 경로

            if path.is_file():
                found.append(path)
            else:
                missing.append(f'{folder}/{name}')

    if missing:
        pp('파일이 없습니다.')

        for name in missing:
            pp('누락된 파일',name)

        return []

    return found


# y sr 로드
def load_y_sr(path):
    y, sr = librosa.load(path, sr=None, mono=False)
    return y, sr


# 파일명, 길이(초), 샘플링레이트, 채널 수를 조사하세요.
def inspect(name, y, sr):

    if y.size == 0 or sr <= 0 or not np.isfinite(y).all():
        raise ValueError('비어있거나 유효하지 않음')

    return {
        'filename': name,
        'duration': round(y.shape[-1] / sr,3), # 재생 시간 (초)
        'sr': sr,
        'channels': 1 if y.ndim == 1 else y.shape[0] # 채널 수
    }


# 피크 진폭(peak)과 RMS 음량 지표를 구하세요.
def peak_rms(y):
    peak = np.max(np.abs(y))
    rms = np.sqrt(np.mean(y ** 2))

    return peak, rms


# 피크 0.03 미만은 recheck, 나머지는 ok로 분류하세요.
# (0.03은 연습용 임계값이므로 실제 방송 적합성 판정은 아닙니다.)
def re_ok(peak):

    if peak < 0.03:
        return 'recheck'
    else:
        return 'ok'


# store_audio_check.csv로 결과를 저장하세요.
def save_check(rows):
    SAVE.mkdir(exist_ok=True)

    fields = [
        'filename','duration','sr','channels','peak','rms','status'
    ]

    report = SAVE / 'store_audio_check.csv'

    with report.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    return report


# 원본 WAV는 수정하지 마세요.

# 결과물
# store_audio_check.csv: 파일별 길이·샘플링레이트·채널·피크·RMS·상태
# 콘솔에 파일별 검사 결과 출력
def main():

    recordings = find_recordings()
    if not recordings:
        return

    rows = []

    for path in recordings:
        y, sr = load_y_sr(path)
        info = inspect(path.name, y, sr)
        peak, rms = peak_rms(y)
        status = re_ok(peak)

        info['peak'] = round(float(peak), 5)
        info['rms'] = round(float(rms), 5)
        info['status'] = status

        rows.append(info)
        pp(
            info['filename'],
            f"길이: {info['duration']}초",
            f"샘플링레이트: {info['sr']}Hz",
            f"채널: {info['channels']}",
            f"Peak: {info['peak']}",
            f"RMS: {info['rms']}",
            f"상태: {info['status']}"
        )

    report = save_check(rows)
    pp(f'CSV 저장 위치: {report}')


if __name__ == '__main__':
    main()