# day24_application.py
# 주제:대출 연체 위험 분류에서 Dropout 효과 분석
#
# 금융 고객의 대출 연체 위험을 가정한 이진 분류 문제를 구성하십시오.
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import make_moons, make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from util.print_util import pp
from include.graph_config import set_graph

set_graph(10, 8, 13)
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE) # NumPy 난수 재현
tf.random.set_seed(RANDOM_STATE) # TensorFlow 난수 재현

# 요구사항
# make_classification()으로 샘플 2,000개, 특성 16개인 데이터를 생성합니다.
X, y = make_classification(
    n_samples=2000,
    n_features=16,
    random_state=RANDOM_STATE,
)
# Training/Validation/Test로 데이터를 분리하고 StandardScaler를 적용합니다.
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
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)
# 은닉층은 Dense(128) → Dense(64) → Dense(32) 구조로 구성합니다.
def build_model_a():
    model = keras.Sequential([
        keras.layers.Input(shape=(16,)),
        keras.layers.Dense(128, activation='relu'),
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

def build_model_b():
    model = keras.Sequential([
        keras.layers.Input(shape=(16,)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dropout(
        0.4, # 학습 중 약 40%의 출력을 제거
        seed=RANDOM_STATE,
        name="dropout_hidden1"
    ),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dropout(
        0.2, # 학습 중 약 20%의 출력을 제거
        seed=RANDOM_STATE,
        name="dropout_hidden2"
    ),
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

# 아래 두 모델을 동일한 조건으로 비교합니다.
# 모델 A: Dropout 없음
model_a = build_model_a()
# 모델 B: 첫 번째 은닉층 뒤에 Dropout(0.4), 두 번째 은닉층 뒤에 Dropout(0.2) 적용
model_b = build_model_b()
# 두 모델 모두 epochs=180, batch_size=32, Adam(0.001)을 사용합니다.
history_a = model_a.fit(
    X_train,
    y_train,
    epochs=180,
    batch_size=32,
    validation_data=(X_val, y_val),
    verbose=0,
)
history_b = model_b.fit(
    X_train,
    y_train,
    epochs=180,
    batch_size=32,
    validation_data=(X_val, y_val),
    verbose=0,
)
# EarlyStopping은 사용하지 않습니다.
# 각 모델의 마지막 Train Accuracy, Validation Accuracy, 두 값의 차이(Gap)를 계산합니다.
train_acc_a = history_a.history['accuracy'][-1]
val_acc_a = history_a.history['val_accuracy'][-1]
gap_a = abs(train_acc_a - val_acc_a)

train_acc_b = history_b.history['accuracy'][-1]
val_acc_b = history_b.history['val_accuracy'][-1]
gap_b = abs(train_acc_b - val_acc_b)

pp('모델 A Train Accuracy:', train_acc_a)
pp('모델 A Validation Accuracy:', val_acc_a)
pp('모델 A Gap:', gap_a)

pp('모델 B Train Accuracy:', train_acc_b)
pp('모델 B Validation Accuracy:', val_acc_b)
pp('모델 B Gap:', gap_b)
# 두 모델의 val_loss를 하나의 그래프로 비교합니다.
plt.plot(history_a.history['val_loss'], label='validation loss')
plt.plot(history_b.history['val_loss'], label='validation loss')
plt.xlabel('model_a_loss')
plt.ylabel('model_b_Loss')
plt.legend()
plt.show()

# Validation Accuracy와 Gap을 함께 고려해 더 적절한 모델을 선택합니다.
if val_acc_b >= val_acc_a and gap_b <= gap_a:
    best_model = model_b
    best_name = 'B'
else:
    best_model = model_a
    best_name = 'A'


test_loss, test_accuracy = best_model.evaluate(
    X_test,
    y_test,
    verbose=0
)

pp('선택 모델:', best_name)
pp('Test Accuracy:', test_accuracy)
# 제출 포인트
# Dropout이 항상 정확도를 높이는 기법이라고 단정하지 말고, 일반화 성능 관점에서 결과를 해석하십시오.
# 제출 포인트
# Dropout 모델의 Validation Accuracy와 Train-Validation Gap을 함께 비교했습니다.
# Dropout은 정확도 자체보다 과적합 완화와 일반화 성능 관점에서 판단해야 합니다.