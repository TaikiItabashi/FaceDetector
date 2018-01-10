from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Conv2D
from keras.layers import Activation, Dropout, Flatten, Dense, BatchNormalization
from keras.utils import np_utils
from keras.optimizers import SGD
from keras.initializers import TruncatedNormal, Constant
import numpy as np
import cv2

#分類対象のカテゴリー
categories = [
    "Kousaka Honoka", "Sonoda Umi", "Minami Kotori",
    "Nishikino Maki", "Koizumi Hanayo", "Hoshizora Rin",
    "Ayase Eli", "Toujou Nozomi", "Yazawa Nico", "other"
]
nb_classes = len(categories)
image_size = 224

#データをロード
def main():
    with np.load("10class.npz") as data:
        X_train = data["a"]
        X_test = data["b"]
        y_train = data["c"]
        y_test = data["d"]
    # X_train, X_test, y_train, y_test = np.load("10class.npz")
    #データを正規化
    X_train = X_train.astype("float") / 256
    X_test = X_test.astype("float") / 256
    y_train = np_utils.to_categorical(y_train, nb_classes)
    y_test = np_utils.to_categorical(y_test, nb_classes)
    model = model_train(X_train, y_train)
    model_eval(model, X_test, y_test)

def conv2d(filters, kernel_size, strides=1, bias_init=1, **kwargs):
    trunc = TruncatedNormal(mean=0.0, stddev=0.01)
    cnst = Constant(value=bias_init)
    return Conv2D(
        filters,
        kernel_size,
        strides=strides,
        padding='same',
        activation='relu',
        kernel_initializer=trunc,
        bias_initializer=cnst,
        **kwargs
    )

def dense(units, **kwargs):
    trunc = TruncatedNormal(mean=0.0, stddev=0.01)
    cnst = Constant(value=1)
    return Dense(
        units,
        activation='tanh',
        kernel_initializer=trunc,
        bias_initializer=cnst,
        **kwargs
    )

#モデルを構築
def build_model(in_shape):
    model = Sequential()

    # 第1畳み込み層
    model.add(conv2d(96, 11, strides=(4,4), bias_init=0, input_shape=in_shape))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
    model.add(BatchNormalization())

    # 第２畳み込み層
    model.add(conv2d(256, 5, bias_init=1))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
    model.add(BatchNormalization())

    # 第３~5畳み込み層
    model.add(conv2d(384, 3, bias_init=0))
    model.add(conv2d(384, 3, bias_init=1))
    model.add(conv2d(256, 3, bias_init=1))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
    model.add(BatchNormalization())

    # 密結合層
    model.add(Flatten())
    model.add(dense(4096))
    model.add(Dropout(0.5))
    model.add(dense(4096))
    model.add(Dropout(0.5))

    # 読み出し層
    model.add(Dense(nb_classes, activation='softmax'))

    model.compile(optimizer=SGD(lr=0.01), loss='categorical_crossentropy', metrics=['accuracy'])
    return model

#モデルを訓練
def model_train(X, y):
    model = build_model(X.shape[1:])
    model.fit(X, y, batch_size=32, epochs=40)
    #モデルを保存
    hdf5_file = "facedetector_model_tenclass.hdf5"
    model.save_weights(hdf5_file)
    return model

#モデルを評価
def model_eval(model, X, y):
    score = model.evaluate(X, y)
    print('loss', score[0])
    print('accuracy=', score[1])

if __name__ == "__main__":
    main()
