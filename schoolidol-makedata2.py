
import os, glob
import numpy as np
import cv2
import random, math

#categories target
root_dir = "train_image"
categories = [
    "Kousaka Honoka", "Sonoda Umi", "Minami Kotori",
    "Nishikino Maki", "Koizumi Hanayo", "Hoshizora Rin",
    "Ayase Eli", "Toujou Nozomi", "Yazawa Nico", "other"
]

nb_classes = len(categories)
image_size = 224

#read image data
X = []  #image data
Y = []  #label data
def add_sample(cat, fname, is_train):
    img = cv2.imread(fname, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (image_size, image_size), interpolation=cv2.INTER_CUBIC)
    data = np.asarray(img)
    X.append(data)
    Y.append(cat)
    if not is_train: return

    #re-angle
    for ang in range(-15, 15, 30):
        rows= img.shape[0]
        cols = img.shape[1]
        M = cv2.getRotationMatrix2D((cols/2,rows/2),ang,1)
        dst = cv2.warpAffine(img,M,(cols,rows))
        data = np.asarray(dst)
        X.append(data)
        Y.append(cat)

    # #reverse
    # dst = cv2.flip(img, 1)
    # data = np.asarray(dst)
    # X.append(data)
    # Y.append(cat)

def make_sample(files, is_train):
    global X, Y
    X = []
    Y = []
    for cat, fname in files:
        add_sample(cat, fname, is_train)
    return np.array(X), np.array(Y)

#collect
allfiles = []
for idx, cat in enumerate(categories):
    image_dir = root_dir + "/" + cat
    files = glob.glob(image_dir + "/*.jpg")
    print(image_dir)
    print(str(len(files)))
    for f in files:
        allfiles.append((idx, f))

#shuffle, devide traindata-testdata
random.shuffle(allfiles)
th = int(math.floor(len(allfiles) * 0.6))
train = allfiles[0:th]
test = allfiles[th:]
X_train, y_train = make_sample(train, True)
X_test, y_test = make_sample(test, False)
xy = (X_train, X_test, y_train, y_test)
print("-----------------------------")
print("train data:" + str(len(X_train)))
print("train label:" + str(len(y_train)))
print("test data:" + str(len(X_test)))
print("test label:" + str(len(y_test)))
np.savez_compressed("10class.npz", a=X_train, b=X_test, c=y_train, d=y_test )
print("ok", len(y_train))
