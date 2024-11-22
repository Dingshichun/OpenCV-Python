# Created by DSC
"""
检测角度。
总体思路是加载图像，鼠标首先点击角点，再点击其余两点，最后求出角度。
"""
import cv2
import math

path = "angle.png"
img = cv2.imread(path)

pointsLists = []


def mousePoints(event, x, y, flag, params):
    """鼠标点击角点获取其坐标，并画出线和点。需要先点击角点，再点其余两点。"""
    if event == cv2.EVENT_LBUTTONDOWN:
        size = len(pointsLists)
        if size != 0 and size % 3 != 0:
            cv2.line(
                img,
                tuple(pointsLists[round((size - 1) / 3) * 3]),
                (x, y),
                (0, 0, 255),
                2,
            )
        cv2.circle(img, (x, y), 5, (0, 0, 255), cv2.FILLED)
        pointsLists.append([x, y])


def gradient(pt1, pt2):
    """根据一条直线上的两个点获取其斜率"""
    return (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])


def getAngle(pointLists):
    """根据两直线的斜率获取夹角"""
    pt1, pt2, pt3 = pointLists[-3:]  # 三个点
    m1 = gradient(pt1, pt2)  # pt1 是角点，m1 和 m2 是两条直线的斜率
    m2 = gradient(pt1, pt3)
    angR = math.atan((m2 - m1) / (1 + (m2 * m1)))  # 得到弧度制的角度
    angD = round(math.degrees(angR))  # 常规角度

    cv2.putText(
        img,
        str(angD),
        (pt1[0] - 40, pt1[1] - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (0, 0, 255),
        2,
    )


while True:
    if len(pointsLists) != 0 and len(pointsLists) % 3 == 0:
        getAngle(pointsLists)
    cv2.imshow("img", img)
    cv2.setMouseCallback("img", mousePoints)

    # 按 r 键重新加载图片
    # if cv2.waitKey(1) & 0xFF == ord("r"):
    #     pointsLists = []
    #     img = cv2.imread(path)

    # 按 q 退出
    if cv2.waitKey(1) == ord("q"):
        break
cv2.destroyAllWindows()
