import cv2
import os

#読み込んだ動画の全フレームを画像ファイルに書き出す
foldername = "callandresponse/"
#フォルダの有無を確認→なければ作る
if not os.path.exists(foldername):
    os.mkdir(foldername)

movie_path = "video/callandresponse.mp4"
cap = cv2.VideoCapture(movie_path)
#フレームの書き出し→保存
snumber = 0
while(cap.get(7) > snumber):
    ret, frame = cap.read()
    print(foldername + str('%04d' % snumber) + ".jpg")
    cv2.imwrite(foldername + str('%04d' % snumber) + ".jpg", frame)
    snumber += 1
cap.release()
