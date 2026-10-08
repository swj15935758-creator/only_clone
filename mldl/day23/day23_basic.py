# day23_basic.py

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from util.print_util import pp, up

keras.utils.set_random_seed(42)

X = np.array([
    [0.10, 0.20], [0.18, 0.30], [0.25, 0.25], [0.32, 0.40],
    [0.40, 0.35], [0.48, 0.50], [0.55, 0.45], [0.62, 0.60],
    [0.70, 0.55], [0.78, 0.70], [0.86, 0.75], [0.95, 0.85]
], dtype=np.float32)
pp(X.shape) # (12, 2)

y = np.array([
    0.18, 0.25, 0.27, 0.36, 0.40, 0.49,
    0.51, 0.62, 0.64, 0.76, 0.83, 0.93
], dtype=np.float32)
pp(y.shape) # (12,)

# 시퀀셜 모델 생성
model = keras.Sequential([
    layers.Input(shape=(2,)), # 거리 비율, 물품량 비율 두 특성을 한 건의 입력으로 사용
    # 은닉층, 뉴런 6개, 층의 이름은 hidden
    layers.Dense(6, activation='relu', name='hidden'),
    layers.Dense(1, name='delivery_time'), # 출력층
], name='delivery_model') # 시퀀셜 모델명

model.summary(print_fn=lambda line: pp(line))

manual_params = (2*6 + 6) + (6*1 + 1) # 25
pp('직접 계산한 파라미터 수: ', manual_params)
pp('Keras 파라미터 수: ', model.count_params())

# 모델 설정
model.compile(
    optimizer='adam', # 최적화 함수, MSE를 줄이는 방향으로 weight, bias 갱신
    loss='mse', # 배송시간 비율의 실제값과 예측값 차이를 제곱해 평균
)

# 학습
history = model.fit(
    X,
    y,
    epochs=200, # 전체 입력데이터 반복 회수
    verbose=0 # 출력 레벨
)

pp(f'첫 Loss: {history.history["loss"][0]:.6f}')
pp(f'마지막 Loss: {history.history["loss"][-1]:.6f}')

new_order = np.array([[0.68, 0.65]], dtype=np.float32)

# 예측, 결과 출력
prediction = model.predict(new_order, verbose=0)[0, 0]
pp(f'예상 배송시간 비율: {prediction:.3f}')

up(5)












