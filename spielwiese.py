import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
from config import classes
from PIL import Image
import keras
import tensorflow as tf
import datetime
import sys

done = False

def findLargestContours(img):
    canny = cv2.Canny(img,0,150)
    kernel = np.ones((3,3),np.uint8)
    
    dilated = cv2.dilate(canny,kernel,iterations=1)
    cv2.imshow('dilated1',dilated)
    eroded = cv2.erode(dilated,kernel,iterations=1)
    cv2.imshow('eroded',eroded)
    cv2.imshow('dilated2',dilated)

    _, contours, _ = cv2.findContours(eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    for c in contours:
        if cv2.contourArea(c) >= 2000:
            _,_,w,h = cv2.boundingRect(c)
            if w/h >= 0.55 and w/h <= 0.85:
                rects.append(c)
    return rects

def drawRoI(img,rects):
    for rect in rects:
        x,y,w,h = cv2.boundingRect(rect)
        cv2.rectangle(img,(x,y),(x+w+10,y+h+10),(0,255,0),2)

def extractRoI(img, rect):
    x,y,w,h = cv2.boundingRect(rect)
    if y > 3 and x > 3:
        cropImg = img[y-3:y+h+3,x-3:x+w+3]
    else:
        cropImg = img[y:y+h,x:x+w]
    cropImgGray = cv2.cvtColor(cropImg,cv2.COLOR_BGR2GRAY)
    return cropImgGray

def doImg(imgPath):
    if os.path.exists(imgPath):
        img = cv2.imread(imgPath)
        src_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = findLargestContours(src_gray)
        cv2.imshow('img',img)
        if len(rects) > 0:
            count = 0
            for rect in rects:
                cropImg = extractRoI(img,rect)
                temp = Image.fromarray(cropImg).resize((146,204))
                cropImgArray = np.array(temp) / 255.0
                if np.argmax(model2.predict(cropImgArray.reshape([1,146,204,1]))) == 0:
                    cv2.imshow('crop',cropImg)
                    temp.save('E:\\Python\\img'+str(count)+'.jpg')
                    count += 1
                    print(np.argmax(model1.predict(cropImgArray.reshape([1,146,204,1]))))
                    print(model1.predict(cropImgArray.reshape([1,146,204,1])))
                    print(classes[str(np.argmax(model1.predict(cropImgArray.reshape([1,146,204,1]))))])
                    drawRoI(img, [rect])
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
    else:
        print('klappt nicht')

def doWebcam():
    cv2.namedWindow('webcam')
    done = False

    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        src_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        src_gray = cv2.blur(src_gray, (3,3))
        #rects = findLargestContours(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY))
        rects = findLargestContours(src_gray)
    
        if len(rects) > 0:
            for rect in rects:
                cropImg = extractRoI(frame,rect)
                temp = Image.fromarray(cropImg).resize((146,204))
                cropImgArray = np.array(temp) / 255.0
                if np.argmax(model2.predict(cropImgArray.reshape([1,146,204,1]))) == 0:
                    if not done:
                        temp.save('E:\\Python\\img.jpg')
                        print('Hallo')
                        done = True
                    else:
                        print('done')
                    cv2.imshow('crop',cropImg)
                    print(np.argmax(model1.predict(cropImgArray.reshape([1,146,204,1]))))
                    print(classes[str(np.argmax(model1.predict(cropImgArray.reshape([1,146,204,1]))))])
                    drawRoI(frame, [rect])
        cv2.imshow('webcam',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    model1 = keras.models.load_model('E:\\Python\\Bachelor\\')
    model2 = keras.models.load_model('E:\\Python\\Bachelor\\CardDetectionModel\\')
    if '-webcam' in sys.argv:
        doWebcam()
    elif '-img' in sys.argv:
        imgPath = sys.argv[sys.argv.index('-img')+1]
        doImg(imgPath)
    
    
