import numpy as np
import os
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
import matplotlib.pyplot as plt
from sklearn.metrics import multilabel_confusion_matrix
from tensorflow.keras.models import load_model


os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

# 필요한 action ---- 주먹, 다핌, 검지중지, 엄지검지, 엄지중지, 엄지소지만, 소지만 ---- 7개
actions = ['rock', 'paper', 'scissors', 'ring_pinky', 'index_middle_ring', 'thumb_index', 'thumb_pinky', 'index_pinky', 'index_right', 'pinky']

# dataset 로드하는 부분
data = np.concatenate([
    np.load('dataset/seq_rock_1691368369.npy'),
    np.load('dataset/seq_paper_1691368369.npy'),
    np.load('dataset/seq_scissors_1691368369.npy'),
    np.load('dataset/seq_ring_pinky_1691368369.npy'),
    np.load('dataset/seq_index_middle_ring_1691368369.npy'),
    np.load('dataset/seq_thumb_index_1691368369.npy'),
    np.load('dataset/seq_thumb_pinky_1691368369.npy'),
    np.load('dataset/seq_index_pinky_1691368369.npy'),
    np.load('dataset/seq_index_right_1691368369.npy'),
    np.load('dataset/seq_pinky_1691368369.npy')
], axis=0)

# print(data.shape) # (x, 30, 100)

x_data = data[:, :, :-1]    # x, 30, 99      
labels = data[:, 0, -1]     # x,

# print(x_data.shape)         # x, 30, 99
# print(labels.shape)         # x,

y_data = to_categorical(labels, num_classes=len(actions))
# print(y_data.shape)       # x, n

x_data = x_data.astype(np.float32)
y_data = y_data.astype(np.float32)

x_train, x_val, y_train, y_val = train_test_split(x_data, y_data, test_size=0.2, random_state=2023)

# print(x_train.shape, y_train.shape)    훈련세트
# print(x_val.shape, y_val.shape)        검증세트

# x_train.shape[1:3] --->  (None, 30, 99)

model = Sequential([
    LSTM(100, activation='relu', input_shape=x_train.shape[1:3]),
    Dense(50, activation='relu'),
    Dense(len(actions), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
# model.summary()

# model training
history = model.fit(
    x_train,
    y_train,
    validation_data=(x_val, y_val),
    epochs=70,
    callbacks=[
        ModelCheckpoint('models/model.h5', monitor='val_acc', verbose=1, save_best_only=True, mode='auto'),
        ReduceLROnPlateau(monitor='val_acc', factor=0.5, patience=50, verbose=1, mode='auto')
    ]
)

# show graph
fig, loss_ax = plt.subplots(figsize=(16, 10))
acc_ax = loss_ax.twinx()

loss_ax.plot(history.history['loss'], 'y', label='train loss')
loss_ax.plot(history.history['val_loss'], 'r', label='val loss')
loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('loss')
loss_ax.legend(loc='upper left')

acc_ax.plot(history.history['acc'], 'b', label='train acc')
acc_ax.plot(history.history['val_acc'], 'g', label='val acc')
acc_ax.set_ylabel('accuracy')
acc_ax.legend(loc='upper left')

plt.show()

# predict actions
model = load_model('models/model.h5')

y_pred = model.predict(x_val)

multilabel_confusion_matrix(np.argmax(y_val, axis=1), np.argmax(y_pred, axis=1))