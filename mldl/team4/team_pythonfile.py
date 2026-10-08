# team4_starter.py
from util.print_util import pp

# 센서 이상 징후 판별 - SimpleRNN vs LSTM 미니프로젝트

# 파일 경로를 처리하기 위해 Path를 가져옵니다.
from pathlib import Path

# 배열 처리를 위해 NumPy를 가져옵니다.
import numpy as np

# 그래프를 그리기 위해 matplotlib을 가져옵니다.
import matplotlib.pyplot as plt

# 데이터 분리를 위해 함수를 가져옵니다.
from sklearn.model_selection import train_test_split

# 분류 평가를 위해 함수를 가져옵니다.
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay

# TensorFlow Keras를 가져옵니다.
from tensorflow import keras


# 난수 시드를 고정합니다.
keras.utils.set_random_seed(42)


# NPZ 파일 경로를 지정합니다.
DATA_FILE = Path(__file__).resolve().parent / "team4_data.npz"


# 데이터를 읽습니다.
data = np.load(DATA_FILE)


# 입력 시퀀스를 가져옵니다.
X = data["X"]

# 정답을 가져옵니다.
y = data["y"]


# TODO 1. X.shape와 y.shape를 출력하세요.
pp('X.shape', X.shape)
pp('y.shape', y.shape)

pp('X 샘플 수: ', X.shape[0])
pp('y 샘플 수: ', y.shape[0])

pp('X 결측치 개수: ', np.isnan(X).sum())
pp('y 결측치 개수: ', np.isnan(y).sum())

pp('X 무한대 값: ', np.isinf(X).sum())
pp('y 무한대 값: ', np.isinf(y).sum())


# 중복 샘플 확인
X_flat = X.reshape(X.shape[0], -1)
unique_X = np.unique(X_flat, axis=0)

pp(f'전체 샘플 수: {X.shape[0]}')
pp(f'고유 샘플 수: {unique_X.shape[0]}')
pp(f'중복 샘플 수: {X.shape[0] - unique_X.shape[0]}')


# TODO 2. samples, timesteps, features의 의미를 설명하세요.

pp('samples', X.shape[0])
pp('timesteps', X.shape[1])
pp('features', X.shape[2])

# samples   : 전체 데이터 샘플의 개수 -> 900개
# timesteps : 하나의 샘플 안에 들어있는 시간 순서의 개수 -> 20개 시점
# features  : 각 시점마다 측정되는 센서값의 개수 -> 3개 센서


# TODO 3. Train/Test를 75:25로 분리하세요.
# stratify=y를 사용하세요.

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

pp('X_train.shape', X_train.shape)
pp('y_train.shape', y_train.shape)
pp('X_test.shape', X_test.shape)
pp('y_test.shape', y_test.shape)


# TODO 4. SimpleRNN(24) 기반 모델을 만드세요.

rnn_model = keras.Sequential([
    keras.layers.Input(shape=(20, 3)),
    keras.layers.SimpleRNN(24),
    keras.layers.Dense(1, activation='sigmoid')
])


# TODO 5. LSTM(24) 기반 모델을 만드세요.

lstm_model = keras.Sequential([
    keras.layers.Input(shape=(20, 3)),
    keras.layers.LSTM(24),
    keras.layers.Dense(1, activation='sigmoid')
])


pp("SimpleRNN 모델")
rnn_model.summary()

pp("LSTM 모델")
lstm_model.summary()


# TODO 6.
# 두 모델 모두 Dense(1, sigmoid)를 출력층으로 사용


# TODO 7.
# 두 모델을 같은 Adam, binary_crossentropy, accuracy 조건으로 compile

rnn_model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

lstm_model.compile(
    optimizer='adam',              # 학습하면서 가중치 조정
    loss='binary_crossentropy',     # 이진 분류에서 오차 계산
    metrics=['accuracy']            # 정확도 확인
)


# TODO 8.
# 같은 EarlyStopping 설정으로 학습

rnn_early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

lstm_early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)


# SimpleRNN 학습
rnn_history = rnn_model.fit(
    X_train,
    y_train,
    validation_split=0.2,
    epochs=100,
    batch_size=32,
    callbacks=[rnn_early_stopping],
    verbose=1
)


# LSTM 학습
lstm_history = lstm_model.fit(
    X_train,
    y_train,
    validation_split=0.2,
    epochs=100,
    batch_size=32,
    callbacks=[lstm_early_stopping],
    verbose=1
)


# TODO 9.
# 두 모델의 count_params(), 실제 Epoch 수,
# val_loss, val_accuracy 비교

pp('RNN 파라미터 수: ', rnn_model.count_params())
pp('LSTM 파라미터 수: ', lstm_model.count_params())

pp('RNN 실제 Epoch 수: ', len(rnn_history.history['loss']))
pp('LSTM 실제 Epoch 수: ', len(lstm_history.history['loss']))

pp('RNN 마지막 val_loss: ',
   rnn_history.history['val_loss'][-1])

pp('RNN 마지막 val_accuracy: ',
   rnn_history.history['val_accuracy'][-1])

pp('LSTM 마지막 val_loss: ',
   lstm_history.history['val_loss'][-1])

pp('LSTM 마지막 val_accuracy: ',
   lstm_history.history['val_accuracy'][-1])


# 가장 좋은 검증 성능 확인
pp(
    f"RNN 최소 val_loss: "
    f"{min(rnn_history.history['val_loss'])}"
)

pp(
    f"RNN 최대 val_accuracy: "
    f"{max(rnn_history.history['val_accuracy'])}"
)

pp(
    f"LSTM 최소 val_loss: "
    f"{min(lstm_history.history['val_loss'])}"
)

pp(
    f"LSTM 최대 val_accuracy: "
    f"{max(lstm_history.history['val_accuracy'])}"
)


# TODO 10.
# 최종 선택 모델의 혼동행렬 출력

# LSTM을 최종 모델로 선택했다고 가정
y_pred_prob = lstm_model.predict(
    X_test,
    verbose=0
)

# sigmoid 확률을 0 / 1로 변환
y_pred = (
    y_pred_prob >= 0.5
).astype(int).ravel()


# 정확도 확인
test_acc = accuracy_score(
    y_test,
    y_pred
)

pp(f'LSTM Test Accuracy: {test_acc:.4f}')


# 혼동행렬
ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred
)

plt.title('LSTM Confusion Matrix')
plt.show()