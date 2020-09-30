from keras import models
import numpy as np
from PIL import Image
import cv2
from roi import findLargestContours, extractRoI, drawRoI

import os
import sys

import requests
import json
from io import BytesIO

import matplotlib.pyplot as plt

import webbrowser

def loadLabels(filepath):
    labelClasses = {}
    i = 0
    for item in os.listdir(filepath):
        labelClasses[i] = item
        i += 1
    return labelClasses

def loadAllModels():
    CardDetectionModel = models.load_model("CardDetectionModel")
    CardDetectionLabels = loadLabels("CardDetectionData")

    SetDetectionModel = models.load_model("SetDetectionModel")
    SetDetectionLabels = loadLabels("SetDetectionData")

    NumberDetectionModel = models.load_model("NumberDetectionModel")
    NumberDetectionLabels = loadLabels("NumberDetectionData")

    myModels = [CardDetectionModel, SetDetectionModel, NumberDetectionModel]
    myLabels = [CardDetectionLabels, SetDetectionLabels, NumberDetectionLabels]
    return myModels, myLabels

def predictCard(card, myModels, myLabels, cardPath=None):
    if not cardPath == None and card == None:
        _img = Image.open(cardPath)
    else:
        _img = card
    cv2.imshow("ROI", np.array(_img))
    w, h = _img.size
    if w != 146 or h != 204:
        _img = _img.resize((146, 204))

    _imgArray = np.array(_img.convert("L")) * 1.0 / 255
    _imgArray1 = _imgArray.reshape([1, 204, 146, 1])
    _imgArray2 = _imgArray.reshape([1, 146, 204, 1])
    print(
        np.argmax(myModels[0].predict(_imgArray2)),
        myLabels[0][np.argmax(myModels[0].predict(_imgArray2))],
    )
    if myLabels[0][np.argmax(myModels[0].predict(_imgArray2))] == "card":
        setPrediction = myLabels[1][np.argmax(myModels[1].predict(_imgArray2))]
        numberPrediction = myLabels[2][np.argmax(myModels[2].predict(_imgArray2))]
        print(f"Prediction - Set : {setPrediction} - Number : {numberPrediction}")
        _img.show()
        return setPrediction, numberPrediction
    else:
        return None, None

def doImg(img, myModels, myLabels):
    cv2.namedWindow("img")
    _img = cv2.imread(img)
    src_gray = cv2.cvtColor(_img, cv2.COLOR_BGR2GRAY)
    src_gray = cv2.blur(src_gray, (3, 3))
    cv2.imshow('img',_img)  
    rects = findLargestContours(src_gray)
    if len(rects) > 0:
        for rect in rects:
            cropImg = extractRoI(_img, rect)
            temp = Image.fromarray(cropImg).resize((146, 204))
            cropImgArray = np.array(temp) / 255.0
            if (
                np.argmax(
                    myModels[0].predict(cropImgArray.reshape([1, 146, 204, 1]))
                )
                == 0
            ):
                plt.imshow(cropImgArray)
                plt.show()
                print(
                    "Set :",
                    myLabels[1][
                        np.argmax(
                            myModels[1].predict(
                                cropImgArray.reshape([1, 204, 146, 1])
                            )
                        )
                    ],
                )
                print(
                    "Number :",
                    myLabels[2][
                        np.argmax(
                            myModels[2].predict(
                                cropImgArray.reshape([1, 204, 146, 1])
                            )
                        )
                    ],
                )
                drawRoI(_img, [rect])
    cv2.imshow("Image", _img)
    cv2.destroyAllWindows()

def doWebcam(myModels, myLabels):
    cv2.namedWindow("webcam")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        src_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        src_gray = cv2.blur(src_gray, (3, 3))
        rects = findLargestContours(src_gray)
        if len(rects) > 0:
            for rect in rects:
                cropImg = extractRoI(frame, rect)
                temp = Image.fromarray(cropImg).resize((146, 204))
                cropImgArray = np.array(temp) / 255.0
                if (
                    np.argmax(
                        myModels[0].predict(cropImgArray.reshape([1, 146, 204, 1]))
                    )
                    == 0
                ):
                    plt.imshow(cropImgArray)
                    plt.show()
                    print(
                        "Set :",
                        myLabels[1][
                            np.argmax(
                                myModels[1].predict(
                                    cropImgArray.reshape([1, 204, 146, 1])
                                )
                            )
                        ],
                    )
                    print(
                        "Number :",
                        myLabels[2][
                            np.argmax(
                                myModels[2].predict(
                                    cropImgArray.reshape([1, 204, 146, 1])
                                )
                            )
                        ],
                    )
                    drawRoI(frame, [rect])
        cv2.imshow("webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    myModels, myLabels = loadAllModels()
    print("\r>>>")
    print("\r>>> MTG - Card Detector started")
    print("\r>>>")
    if "-webcam" in sys.argv:
        doWebcam(myModels, myLabels)
    elif "-cardImg" in sys.argv:
        if len(sys.argv) - 1 > sys.argv.index("-cardImg"):
            _set, _number = predictCard(
                None,
                myModels,
                myLabels,
                cardPath=sys.argv[sys.argv.index("-cardImg") + 1],
            )
            try:
                if not _set == None:
                    webbrowser.open(
                        "https://scryfall.com/card/" + str(_set) + "/" + str(_number)
                    )
                else:
                    print("Die Karte wurde nicht erkannt")
            except Exception as e:
                print(e)
        else:
            print("No image path was specified")
    elif "-img" in sys.argv:
        if len(sys.argv) - 1 > sys.argv.index("-img"):
            doImg(sys.argv[sys.argv.index("-img") + 1], myModels, myLabels)
        else:
            print("No image path was specified")
    else:
        print('')
