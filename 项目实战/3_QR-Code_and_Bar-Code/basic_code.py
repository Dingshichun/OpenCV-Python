# Created by DSC
"""
pyzbar 是生成和识别条形码和二维码的模块
"""

import cv2
import numpy as np
from pyzbar.pyzbar import decode

# 可加载图像或相机采集
# img = cv2.imread('barCode.jpg')
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:

    success, img = cap.read()
    for barcode in decode(img):
        myData = barcode.data.decode("utf-8")  # 解码为 utf-8 格式
        print(myData)
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, (255, 0, 255), 5)
        pts2 = barcode.rect
        cv2.putText(
            img,
            myData,
            (pts2[0], pts2[1]),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 0, 255),
            2,
        )

    cv2.imshow("Result", img)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
