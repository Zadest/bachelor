import cv2
from PIL import Image
import numpy as np


def findLargestContours(img):
    canny = cv2.Canny(img, 0, 130)
    kernel = np.ones((3, 3), np.uint8)

    dilated = cv2.dilate(canny, kernel, iterations=1)
    cv2.imshow("dilated1", dilated)
    eroded = cv2.erode(dilated, kernel, iterations=1)
    cv2.imshow("eroded", eroded)

    _, contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    _, tempcountours, _ = cv2.findContours(
        eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    rects = []
    for c in contours + tempcountours:
        if cv2.contourArea(c) >= 2000:
            _, _, w, h = cv2.boundingRect(c)
            rects.append(c)
    return rects


def drawRoI(img, rects):
    for rect in rects:
        x, y, w, h = cv2.boundingRect(rect)
        cv2.rectangle(img, (x, y), (x + w + 10, y + h + 10), (0, 255, 0), 2)


def extractRoI(img, rect):
    x, y, w, h = cv2.boundingRect(rect)
    if y > 3 and x > 3:
        cropImg = img[y - 3 : y + h + 3, x - 3 : x + w + 3]
    else:
        cropImg = img[y : y + h, x : x + w]
    cropImgGray = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)
    return cropImgGray
