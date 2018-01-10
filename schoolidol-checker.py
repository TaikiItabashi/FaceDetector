import schoolidol_keras as schoolidol
import sys, os, re
from PIL import Image
import numpy as np
import cv2
import glob

#分類機の顔検出用の特徴量
cascade_path = "/usr/local/opt/opencv/share/OpenCV/lbpcascades/lbpcascade_animeface.xml"
color_cat = [(76, 183, 255), (255, 0 ,0), (250, 250, 250),
 (21, 0, 219), (101, 255, 149),(0, 255, 255),
 (22, 196, 183), (204, 0, 196), (15, 143, 239), (0, 0, 0)]

#フォルダの有無を確認→なければ作る
foldername = "yumenotobira_detect/"
if not os.path.exists(foldername):
    os.mkdir(foldername)

image_size = 244
categories = [
    "高坂穂乃果", "園田海未", "南ことり",
    "西木野真姫", "小泉花陽", "星空凛",
    "絢瀬絵里", "東條希", "矢澤にこ", "other"
]

categories_e = [
    "honoka", "umi", "kotori",
    "maki", "hanayo", "rin",
    "eli", "nozomi", "nico", "other"
]

image_path = "yumenotobira/"

#モデルの構築
model = schoolidol.build_model((244, 244, 3))
model.load_weights("facedetector_model_tenclass.hdf5")

#1フレームずつ処理
fnum = 0
file_list = sorted(glob.glob(image_path + "*"))
print(file_list)
for fname in file_list:
    image = cv2.imread(fname)
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    cascade = cv2.CascadeClassifier(cascade_path)
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))

    #検出した顔を予測
    if len(facerect) > 0:
        for rect in facerect:
            X = []
            f_image = image[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]    #顔部分の切り抜き
            if (len(f_image) == 0): continue
            f_image_re = cv2.resize(f_image, (image_size, image_size), interpolation=cv2.INTER_CUBIC)           #モデルに突っ込むimgの作成
            in_data = np.asarray(f_image_re)
            X.append(in_data)
            X = np.array(X).astype("float") / 256

            #データを予測
            pre = model.predict(X)
            detect = categories_e[np.argmax(pre[0])]
            mes = categories_e[np.argmax(pre[0])] + "[" + str(pre[0][np.argmax(pre[0])]) + "]"
            cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color_cat[np.argmax(pre[0])], thickness=2)
            cv2.putText(image, mes, (rect[0], rect[1]), cv2.FONT_ITALIC, 1, color_cat[np.argmax(pre[0])], 1, 4)

    print(foldername + str(fnum) + ".jpg")
    cv2.imwrite(foldername + str(fnum) + ".jpg", image)
    fnum += 1
