from keras import models
import numpy as np
from PIL import Image

import os
import sys

import requests
import json
from io import BytesIO

import matplotlib.pyplot as plt

def loadLabels(filepath):
    labelClasses = {}
    i = 0
    for item in os.listdir(filepath):
        labelClasses[i] = item
        i += 1

    return labelClasses

def loadAllModels():
    model1 = models.load_model('SetRecognitionModelSave')
    labelClass1 = loadLabels('SetDetectionData')
    model2 = models.load_model('NumberRecognitionModel')
    labelClass2 = loadLabels('NumberDetectionData')
    return  model1, model2, labelClass1, labelClass2

def predictCard(cardPath,setNet,numberNet,setClasses,numberClasses):
    _img = Image.open(cardPath)
    w,h = _img.size
    if w != 146 or h != 204:
        _img = _img.resize((146,204))
    _img.show()
    _imgArray = np.array(_img.convert('L')) * 1.0/255
    _imgArray = _imgArray.reshape([1,204,146,1])
    setPrediction = setClasses[np.argmax(setNet.predict(_imgArray))]
    numberPrediction = numberClasses[np.argmax(numberNet.predict(_imgArray))]
    print(f'Prediction - Set : {setPrediction} - Number : {numberPrediction}')

if __name__ == '__main__':
    SetDetectionModel, NumberDetectionModel, setClasses, numberClasses = loadAllModels()
    print('\r>>>')
    print('\r>>> MTG - Card Detector started')
    print('\r>>>')
    if '-img' in sys.argv:      
        if len(sys.argv)-1 > sys.argv.index('-img'):
            predictCard(sys.argv[sys.argv.index('-img')+1],SetDetectionModel, NumberDetectionModel, setClasses, numberClasses)
        else:
            print('No image path was specified')
        