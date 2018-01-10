import cv2
import os, re

#分類機の顔検出用の特徴量
cascade_path = "/usr/local/opt/opencv/share/OpenCV/lbpcascades/lbpcascade_animeface.xml"


#保存先フォルダの有無を確認→なければ作る
foldername = "image/face/"
if not os.path.exists(foldername):
    os.mkdir(foldername)

#顔検出対象の画像があるフォルダ
image_path = "image/"
color = (255, 255, 255)

#image_path内の画像数
files = os.listdir(image_path)
count = 0
for file in files:
    index = re.search('.jpg', file)
    if index:
        count += 1

#顔検出
directory_path_list = os.listdir(image_path)
fnumber = 0
for dp in directory_path_list:
    if dp == "face": continue
    if dp == ".DS_Store": continue
    image_path_list = os.listdir(image_path + dp + "/")
    for fp in image_path_list:
        if fp == ".DS_Store": continue
        try:
            image = cv2.imread(image_path + dp + "/" + fp)
        except:
            continue
        print(image_path + dp + "/" + fp)
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        cascade = cv2.CascadeClassifier(cascade_path)
        facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(100, 100))

        #検出した顔を新たな画像ファイルに保存。100*100にリサイズ
        if len(facerect) > 0:
            for rect in facerect:
                f_image = image[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
                # f_image_re = cv2.resize(f_image, (100, 100))
                # print(foldername + dp + "/" + str(fnumber) + ".jpg")
                cv2.imwrite(foldername + str(fnumber) + ".jpg", f_image)
                fnumber += 1
