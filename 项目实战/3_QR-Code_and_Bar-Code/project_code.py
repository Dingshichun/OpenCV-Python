# Created by DSC
"""
检测条码的内容是否在 myDataFile.txt 文件中
pyzbar 是生成和识别条形码和二维码的模块
"""

import cv2
import numpy as np
from pyzbar.pyzbar import decode  # decode 解码

# img = cv2.imread('barCode.jpg')
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

with open("myDataFile.txt") as f:
    myDataList = f.read().splitlines()  # 按行读取文本内容存到列表

while True:

    success, img = cap.read()
    for barcode in decode(img):
        myData = barcode.data.decode("utf-8")  # 解码为 utf-8 格式
        print(myData)

        # 解码得到的内容是否在文本文件中
        if myData in myDataList:
            myOutput = "Authorized"
            myColor = (0, 255, 0)  # 颜色顺序为 bgr
        else:
            myOutput = "Un-Authorized"
            myColor = (0, 0, 255)

        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, myColor, 5)
        pts2 = barcode.rect
        cv2.putText(
            img, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2
        )

    cv2.imshow("Result", img)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
