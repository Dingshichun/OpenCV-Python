# Created by DSC

"""
对候选框进行非极大值抑制，只保留置信度大于阈值的候选框。
解压 Object_Detection_Files.zip 得到需要的文件。
运行时 i = i[0] 可能会报错。
"""

import cv2
import numpy as np

thres = 0.45  # Threshold to detect object，检测框占目标框的比例
nms_threshold = 0.5
cap = cv2.VideoCapture(0)
# cap.set(3,1280)
# cap.set(4,720)
# cap.set(10,150)

classNames = []
classFile = "./Object_Detection_Files/coco.names"
with open(classFile, "rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

# print(classNames)
configPath = "./Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "./Object_Detection_Files/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

while True:
    success, img = cap.read()
    classIds, confs, bbox = net.detect(img, confThreshold=thres)
    bbox = list(bbox)
    confs = list(np.array(confs).reshape(1, -1)[0])
    confs = list(map(float, confs))
    # print(type(confs[0]))
    # print(confs)

    indices = cv2.dnn.NMSBoxes(bbox, confs, thres, nms_threshold)
    # print(indices)

    for i in indices:

        i = i[0]
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        cv2.rectangle(img, (x, y), (x + w, h + y), color=(0, 255, 0), thickness=2)
        cv2.putText(
            img,
            classNames[classIds[i][0] - 1].upper(),
            (box[0] + 10, box[1] + 30),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (0, 255, 0),
            2,
        )

    cv2.imshow("Output", img)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
