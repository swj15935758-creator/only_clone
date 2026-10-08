# day25_basic.py
# 주차 공간 이미지의 차량 점유 여부 분류

import numpy as np
from tensorflow import keras
from util.print_util import pp, up

np.random.seed(24)
keras.utils.set_random_seed(24)

def make_parking_images(sample_count=600, image_size=20):
    X = np.random.normal(0.08, 0.05, (sample_count, image_size, image_size, 1)).astype("float32")
    y = np.random.randint(0, 2, sample_count).astype("float32")
    for i, label in enumerate(y):
        X[i, 2:-2, 2, 0] += 0.25  # 주차선 왼쪽
        X[i, 2:-2, -3, 0] += 0.25  # 주차선 오른쪽
        X[i, 2, 2:-2, 0] += 0.25  # 주차선 위쪽
        X[i, -3, 2:-2, 0] += 0.25  # 주차선 아래쪽
        if label == 1:
            row_shift = np.random.randint(-1, 2)  # 차량 위치를 조금 변화시킴
            col_shift = np.random.randint(-1, 2)
            r1, r2 = 6 + row_shift, 15 + row_shift
            c1, c2 = 7 + col_shift, 14 + col_shift
            X[i, r1:r2, c1:c2, 0] += 0.75  # 중앙 차량 패턴
    X = np.clip(X, 0.0, 1.0)
    order = np.random.permutation(sample_count)
    return X[order], y[order]

X, y = make_parking_images()

split = int(len(X) * 0.8)

X_train, X_test = X[:split], X[split:]

y_train, y_test = y[:split], y[split:]

pp("전체 shape", X.shape, y.shape)
pp("학습/평가 shape", X_train.shape, X_test.shape)

model = keras.Sequential([
    keras.Input(shape=(20, 20, 1)),  # batch 축을 제외한 단일 이미지 shape
    keras.layers.Conv2D(16, 3, padding="same", activation="relu"),
    keras.layers.MaxPooling2D(2),
    keras.layers.Conv2D(32, 3, padding="same", activation="relu"),
    keras.layers.MaxPooling2D(2),
    keras.layers.Flatten(),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dense(1, activation="sigmoid")
], name="parking_cnn")

summary_lines = []
model.summary(print_fn=summary_lines.append)
pp("모델 구조", "\n".join(summary_lines))

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.fit(
    X_train,
    y_train,
    epochs=6,
    batch_size=32,
    validation_split=0.2,
    verbose=0
)

loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
pp("평가 loss/accuracy", round(float(loss), 4), round(float(accuracy), 4))

prob = model.predict(X_test[:5], verbose=0).reshape(-1)
pred = (prob >= 0.5).astype(int)

pp("실제 클래스", y_test[:5].astype(int))
pp("예측 확률", np.round(prob, 4))
pp("예측 클래스", pred)

up(5)
