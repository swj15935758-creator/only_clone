# day24_challenge.py
# 주제:배송시간 예측 회귀 모델의 Optimizer 설정과 EarlyStopping 비교
#
# 온라인 주문의 배송시간을 예측하는 회귀 문제를 구성하십시오.

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from util.print_util import pp
from include.graph_config import set_graph


set_graph(10, 8, 13)

RANDOM_STATE = 42

np.random.seed(RANDOM_STATE) # NumPy 난수 재현
tf.random.set_seed(RANDOM_STATE) # TensorFlow 난수 재현


# 요구사항
# make_regression()으로 샘플 2,400개, 특성 12개인 회귀 데이터를 생성하고 적절한 잡음을 포함합니다.
X, y = make_regression(
    n_samples=2400,
    n_features=12,
    noise=10,
    random_state=RANDOM_STATE,
)


# Train/Test를 8:2로 분리합니다.
X_train_full, X_test, y_train_full, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=RANDOM_STATE,
)


# Training Set의 20%를 Validation Set으로 추가 분리합니다.
X_train, X_val, y_train, y_val = train_test_split(
    X_train_full,
    y_train_full,
    test_size=0.2,
    random_state=RANDOM_STATE,
)


# 입력 특성에 StandardScaler를 적용합니다.
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)


# Learning Rate만 다르게 사용할 수 있도록 모델 생성 함수 작성
def build_model(learning_rate):

    model = keras.Sequential([
        keras.layers.Input(shape=(12,)),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(32, activation='relu'),

        # 회귀 문제이므로 활성화 함수 없음
        keras.layers.Dense(1)
    ])


    adam = keras.optimizers.Adam(
        learning_rate=learning_rate
    )


    model.compile(
        optimizer=adam,
        loss='mse',
        metrics=['mae']
    )


    return model


# 비교할 Learning Rate
learning_rates = [
    0.0005,
    0.001,
    0.005
]


# 각 실험 결과를 저장할 리스트
results = []

histories = []

models = []


# Learning Rate 3개를 하나씩 실험
for learning_rate in learning_rates:

    # 매 실험마다 새로운 모델 생성
    model = build_model(
        learning_rate
    )


    # 매 실험마다 새로운 EarlyStopping 생성
    early_stopping = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=15,
        min_delta=0.01,
        restore_best_weights=True
    )


    # 모델 학습
    history = model.fit(
        X_train,
        y_train,
        epochs=500,
        batch_size=32,
        validation_data=(X_val, y_val),
        callbacks=[early_stopping],
        verbose=0
    )


    # 실제 수행 Epoch 수
    actual_epochs = len(
        history.history['loss']
    )


    # 가장 낮은 Validation Loss
    best_val_loss = min(
        history.history['val_loss']
    )


    # 가장 낮은 Validation Loss가 나온 위치
    best_index = np.argmin(
        history.history['val_loss']
    )


    # Epoch는 1부터 세기 때문에 +1
    best_epoch = best_index + 1


    # 최저 val_loss가 나온 Epoch의 Validation MAE
    best_val_mae = history.history['val_mae'][best_index]


    # 결과 저장
    results.append({
        'learning_rate': learning_rate,
        'actual_epochs': actual_epochs,
        'best_epoch': best_epoch,
        'best_val_loss': best_val_loss,
        'val_mae': best_val_mae
    })


    histories.append(history)
    models.append(model)


# 결과 출력
for result in results:

    pp('Learning Rate:', result['learning_rate'])
    pp('실제 수행 Epoch:', result['actual_epochs'])
    pp('최저 Validation Loss:', result['best_val_loss'])
    pp('Validation MAE:', result['val_mae'])
    pp('최저 val_loss Epoch:', result['best_epoch'])
    pp('--------------------------------')


# 세 실험의 val_loss 그래프
for index in range(len(learning_rates)):

    plt.plot(
        histories[index].history['val_loss'],
        label=f'LR={learning_rates[index]}'
    )


plt.xlabel('Epoch')
plt.ylabel('Validation Loss')
plt.legend()
plt.show()


# Validation Loss가 가장 작은 실험 찾기
best_result_index = 0

for index in range(1, len(results)):

    if results[index]['best_val_loss'] < results[best_result_index]['best_val_loss']:
        best_result_index = index


best_model = models[best_result_index]

best_result = results[best_result_index]


# 가장 좋은 모델을 Test 데이터로 최종 평가
test_loss, test_mae = best_model.evaluate(
    X_test,
    y_test,
    verbose=0
)


pp('[최종 선택]')
pp('Learning Rate:', best_result['learning_rate'])
pp('실제 수행 Epoch:', best_result['actual_epochs'])
pp('최저 Validation Loss:', best_result['best_val_loss'])
pp('최저 Validation Loss Epoch:', best_result['best_epoch'])

pp('[Test 결과]')
pp('Test MAE:', test_mae)


# Learning Rate가 너무 작으면 Loss가 천천히 감소하여 충분한 학습에 많은 Epoch가 필요할 수 있습니다.
# Learning Rate가 너무 크면 최적값 주변을 지나치면서 Validation Loss가 불안정하게 움직일 수 있습니다.