# day24_basic.py
# 주제: 제조 설비 이상 여부 분류에서 Epoch와 Batch Size 비교
#
# 제조 설비 센서 데이터를 가정한 이진 분류 문제를 구성하십시오.
# import time

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from util.print_util import pp
from include.graph_config import set_graph

# 요구사항
set_graph(10, 8, 13)

RANDOM_STATE = 42

np.random.seed(RANDOM_STATE) # NumPy 난수 재현

tf.random.set_seed(RANDOM_STATE) # TensorFlow 난수 재현


# make_classification()으로 샘플 1,500개, 특성 10개인 이진 분류 데이터를 생성합니다.
X, y = make_classification(
    n_samples=1_500,
    n_features=10,
    random_state=RANDOM_STATE
)


# Train/Test를 8:2로 분리하고, Training Set의 20%를 Validation Set으로 추가 분리합니다.
X_train_full, X_test, y_train_full, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=RANDOM_STATE,
    stratify=y
)

X_train, X_val, y_train, y_val = train_test_split(
    X_train_full,
    y_train_full,
    test_size=0.2,
    random_state=RANDOM_STATE,
    stratify=y_train_full
)


# StandardScaler를 Training Set에 fit하고 Validation/Test에는 transform만 적용합니다.
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)


# Dense 은닉층 2개와 sigmoid 출력층으로 모델을 구성합니다.
def build_model():
    model = keras.Sequential([
        keras.layers.Input(shape=(10,)),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid'),
    ])

    # Optimizer는 Adam, Learning Rate는 0.001로 고정합니다.
    adam = keras.optimizers.Adam(
        learning_rate=0.001
    )

    model.compile(
        optimizer=adam,
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    return model


# A와 B는 서로 다른 모델로 생성
model_a = build_model()
model_b = build_model()

# 두 모델의 시작 가중치를 같게 맞춤
model_b.set_weights(
    model_a.get_weights()
)


# 아래 두 설정을 각각 학습하고 학습시간, 실제 수행 Epoch 수, Validation Accuracy를 비교합니다.

# 설정 A: epochs=30, batch_size=16
# start_time_a = time.perf_counter()

history_a = model_a.fit(
    X_train,
    y_train,
    epochs=30,
    batch_size=16,
    validation_data=(X_val, y_val),
    verbose=0
)
#
# end_time_a = time.perf_counter()
#
# training_time_a = end_time_a - start_time_a


# 설정 B: epochs=60, batch_size=64
# start_time_b = time.perf_counter()

history_b = model_b.fit(
    X_train,
    y_train,
    epochs=60,
    batch_size=64,
    validation_data=(X_val, y_val),
    verbose=0
)

# end_time_b = time.perf_counter()

# training_time_b = end_time_b - start_time_b


# 두 설정 모두 EarlyStopping은 사용하지 않습니다.

# 실제 수행 Epoch 수
epochs_a = len(history_a.history['loss'])
epochs_b = len(history_b.history['loss'])

# 마지막 Validation Accuracy
val_accuracy_a = history_a.history['val_accuracy'][-1]
val_accuracy_b = history_b.history['val_accuracy'][-1]


pp('설정 A')
# pp('학습시간:', training_time_a)
pp('실제 Epoch:', epochs_a)
pp('Validation Accuracy:', val_accuracy_a)

pp('설정 B')
# pp('학습시간:', training_time_b)
pp('실제 Epoch:', epochs_b)
pp('Validation Accuracy:', val_accuracy_b)


# 마지막에 더 적절하다고 판단한 설정의 Test Accuracy를 출력합니다.
if val_accuracy_a >= val_accuracy_b:
    best_model = model_a
    best_name = 'A'
else:
    best_model = model_b
    best_name = 'B'


test_loss, test_accuracy = best_model.evaluate(
    X_test,
    y_test,
    verbose=0
)

pp('선택한 설정:', best_name)
pp('Test Accuracy:', test_accuracy)


# 제출 포인트
# 두 실험에서 Epoch와 Batch Size 외의 조건은 동일하게 유지하십시오.
# Validation Accuracy가 더 높은 설정을 선택하고 최종 Test Accuracy를 확인했습니다.