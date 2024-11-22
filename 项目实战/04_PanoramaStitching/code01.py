# Created by DSC
"""
全景拼接。
解压 Images.zip 压缩包，得到 Images 文件夹，
如果解压得到的是两级 Images 目录，只需要保留一级，不然路径会出错。
"""
import cv2
import os

mainFolder = "Images"
myFolders = os.listdir(mainFolder)
print(myFolders)

for folder in myFolders:
    path = mainFolder + "/" + folder
    images = []
    myList = os.listdir(path)
    print(f"Total no of images detected {len(myList)}")
    for imgN in myList:
        curImg = cv2.imread(f"{path}/{imgN}")
        curImg = cv2.resize(curImg, (0, 0), None, 0.2, 0.2)
        images.append(curImg)

    stitcher = cv2.Stitcher.create()
    (status, result) = stitcher.stitch(images)
    if status == cv2.STITCHER_OK:
        print("Panorama Generated")
        cv2.imshow(folder, result)
        cv2.waitKey(1)
    else:
        print("Panorama Generation Unsuccessful")

cv2.waitKey(0)
