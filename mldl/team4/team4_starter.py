# team4_starter.py
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

from include.graph_config import set_graph
from util.print_util import pp

# 그래프 설정
set_graph(8,8,8)
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
# 1. 데이터 기본 구조 확인
pp("X shape", X.shape)
pp("y shape", y.shape)

pp("X 데이터 타입", X.dtype)
pp("y 데이터 타입", y.dtype)

# 2. X와 y의 샘플 개수가 같은지 확인
pp("X 샘플 수", X.shape[0])
pp("y 정답 수", y.shape[0])
pp("X와 y 개수 일치 여부", X.shape[0] == y.shape[0])

# 3. 결측치(NaN) 확인
pp("X 결측치 개수", np.isnan(X).sum())

# 4. 무한대(inf) 값 확인 이상한 값이 존재 하냐?
pp("X 무한대 개수", np.isinf(X).sum())

# 5. 중복 샘플이 있는지만 확인
is_duplicates = len(X) != len(np.unique(X, axis=0))

pp("중복 여부", is_duplicates)
# TODO 2. samples, timesteps, features의 의미를 설명하세요.
# 1개의 샘플에 20개의 시점 별로 각각 3개의 특성이 있다

# TODO 3. Train/Test를 75:25로 분리하세요.
# stratify=y를 사용하세요.
X_train,X_test,y_train,y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    stratify=y,
    random_state=42
)
# TODO 4. SimpleRNN(24) 기반 모델을 만드세요.
# SimpleRNN 모델 생성
rnn = keras.Sequential([
    keras.Input(shape=(20, 3)),
    keras.layers.SimpleRNN(24),
    keras.layers.Dense(1, activation='sigmoid')
])

rnn.summary()

# TODO 5. LSTM(24) 기반 모델을 만드세요.
lstm = keras.Sequential([
    keras.Input(shape=(20, 3)),
    keras.layers.LSTM(24),
    keras.layers.Dense(1, activation='sigmoid')
])
lstm.summary()

# TODO 6. 두 모델 모두 Dense(1, sigmoid)를 출력층으로 사용하세요.

# TODO 8. 같은 EarlyStopping 설정으로 학습하세요.
rnn_early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss', # 감시할 검증 지표
    patience=5, # 개선 없이 허용할 Epoch 수
    min_delta=0.001, # 이 값 이상 검증손실값이 좋아져야 개선으로 인정
    mode='min', # val_loss 는 값이 작을수록 좋으므로 min 방향으로 설정
    restore_best_weights=True, # 최적의 가중치로 복원
    verbose=1 # 조기 종료 정보를 출력
)


lstm_early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss', # 감시할 검증 지표
    patience=5, # 개선 없이 허용할 Epoch 수
    min_delta=0.001, # 이 값 이상 검증손실값이 좋아져야 개선으로 인정
    mode='min', # val_loss 는 값이 작을수록 좋으므로 min 방향으로 설정
    restore_best_weights=True, # 최적의 가중치로 복원
    verbose=1 # 조기 종료 정보를 출력
)
# TODO 7. 두 모델을 같은 Adam, binary_crossentropy, accuracy 조건으로 compile하세요.
rnn.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

lstm.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# 학습 부분
rnn_history = rnn.fit(
    X_train,
    y_train,
    epochs=100,
    validation_split=0.2,
    callbacks=[rnn_early_stopping],
    verbose=0
)

lstm_history = lstm.fit(
    X_train,
    y_train,
    epochs=100,
    validation_split=0.2,
    callbacks=[lstm_early_stopping],
    verbose=0
)

# *TODO 9. 두 모델의 count_params(), 실제 Epoch 수, val_loss, val_accuracy를 비교하세요.*
pp(f'SIMPLE RNN 파라미터수 KERAS 계산: {rnn.count_params()}') # 697
pp(f'LSTM 파라미터수 KERAS 계산: {lstm.count_params()}') # 2713

pp(f'실제 RNN epoch 횟수: {len(rnn_history.history["loss"])}')
pp(f'실제 LSTM epoch 횟수: {len(lstm_history.history["loss"])}')

pp(f'마지막 RNN val_loss: {rnn_history.history["val_loss"][-1]}')
pp(f'마지막 LSTM val_loss: {lstm_history.history["val_loss"][-1]}')

pp(f'마지막 RNN val_accuracy: {rnn_history.history["val_accuracy"][-1]}')
pp(f'마지막 LSTM val_accuracy: {lstm_history.history["val_accuracy"][-1]}')

# # SimpleRNN 학습 곡선
# plt.plot(
#     rnn_history.history['loss'],
#     label='Train Loss'
# )
#
# plt.plot(
#     rnn_history.history['val_loss'],
#     label='Validation Loss'
# )
#
# plt.title('SimpleRNN 학습 곡선')
# plt.xlabel('Epoch')
# plt.ylabel('Loss')
# plt.legend()
# plt.show()
#
#
# # LSTM 학습 곡선
# plt.plot(
#     lstm_history.history['loss'],
#     label='Train Loss'
# )
#
# plt.plot(
#     lstm_history.history['val_loss'],
#     label='Validation Loss'
# )
#
# plt.title('LSTM 학습 곡선')
# plt.xlabel('Epoch')
# plt.ylabel('Loss')
# plt.legend()
# plt.show()
#
# # *TODO 10. 최종 모델의 혼동행렬을 출력하세요.*
# rnn_pred = rnn.predict(X_test, verbose=0)
# lstm_pred = lstm.predict(X_test, verbose=0)
#
# rnn_pred_class = (rnn_pred >= 0.5).astype(int).flatten()
# lstm_pred_class = (lstm_pred >= 0.5).astype(int).flatten()
#
# pp('RNN 평가 accuracy: ', accuracy_score(y_test, rnn_pred_class))
# pp('LSTM 평가 accuracy: ', accuracy_score(y_test, lstm_pred_class))
#
# ## 혼동 행렬
# # ConfusionMatrixDisplay.from_predictions(
# #     y_test,
# #     rnn_pred_class
# # )
# # plt.title('SimpleRNN 혼동행렬')
# # plt.show()
# #
# # ConfusionMatrixDisplay.from_predictions(
# #     y_test,
# #     lstm_pred_class
# # )
# # plt.title('LSTM 혼동행렬')
# # plt.show()
#
# # 정확도 너무 높아서 확인
# # 클래스 비율이 같음
# pp('0 개수: ', np.sum(y == 0)) #0 개수:  450
# pp('1 개수: ', np.sum(y == 1)) #1 개수:  450
#
# # 평균 확인
# # 시점 별로 높고 낮은건 아닌거 같다
# pp("클래스 0(정상) 평균:", X[y == 0].mean(axis=0))
# pp("클래스 1(비정상) 평균:", X[y == 1].mean(axis=0))
#
# # 선 그래프로 판단
# class_0_mean = X[y == 0].mean(axis=0)
# class_1_mean = X[y == 1].mean(axis=0)
#
# pp("클래스 0(정상) 평균 shape:", class_0_mean.shape)
# pp("클래스 1(비정상) 평균 shape:", class_1_mean.shape)
# for feature in range(3):
#
#     plt.plot(
#         class_0_mean[:, feature],
#         label='클래스 0' # 정상
#     )
#
#     plt.plot(
#         class_1_mean[:, feature],
#         label='클래스 1' # 비정상
#     )
#
#     plt.title(f'특성 {feature} 클래스별 평균')
#     plt.xlabel('시점')
#     plt.ylabel('평균값')
#     plt.legend()
#     plt.show()
#
#     plt.scatter(
#         X[y == 0, 19, 0],
#         X[y == 0, 19, 1],
#         label='클래스 0'
#     )
#
#     plt.scatter(
#         X[y == 1, 19, 0],
#         X[y == 1, 19, 1],
#         label='클래스 1'
#     )
#
#     plt.xlabel('19시점 특성 0')
#     plt.ylabel('19시점 특성 1')
#     plt.legend()
#     plt.show()