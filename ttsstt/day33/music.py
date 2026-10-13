import numpy as np
import soundfile as sf
from pathlib import Path

sr = 22050
bpm = 112
beat = 60 / bpm
notes = [
    ("C4", 0.5), ("E4", 0.5), ("G4", 0.5), ("E4", 0.5),
    ("F4", 0.5), ("A4", 0.5), ("G4", 1.0),
    ("E4", 0.5), ("G4", 0.5), ("C5", 0.5), ("B4", 0.5),
    ("A4", 0.5), ("G4", 0.5), ("C5", 1.0),
]
freqs = {"C4":261.63,"E4":329.63,"F4":349.23,"G4":392.0,"A4":440.0,"B4":493.88,"C5":523.25}
rng = np.random.default_rng(42)

def play_note(freq, duration):
    n = int(sr * duration)
    t = np.arange(n) / sr
    # 악기 음색: 기본 주파수와 고조파
    tone = (np.sin(2*np.pi*freq*t) +
            0.32*np.sin(2*np.pi*2*freq*t) +
            0.12*np.sin(2*np.pi*3*freq*t))
    attack = np.minimum(1, t / 0.012)
    decay = np.exp(-1.7 * t / max(duration, 0.01))
    release = np.minimum(1, (duration-t) / 0.075)
    envelope = attack * decay * np.maximum(release, 0)
    return tone * envelope

y = np.concatenate([play_note(freqs[n], d*beat) for n,d in notes])
# 부드러운 잔향
delay = int(0.17 * sr)
reverb = np.zeros_like(y)
reverb[delay:] = 0.19*y[:-delay]
y = y + reverb
y = (0.85 / np.max(np.abs(y)) * y).astype(np.float32)
path = Path("short_melody.wav")
sf.write(path, y, sr, subtype="PCM_16")
print(f"파일: {path}, 재생시간: {len(y)/sr:.2f}초")
print("처음 20개 샘플:", np.round(y[:20], 4))
