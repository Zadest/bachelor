import cv2 as cv
import numpy as np
from io import BytesIO
import json
from PIL import Image
from keras import models
from keras import layers, losses, preprocessing
import matplotlib.pyplot as plt
import requests
from time import sleep
import random
import os
import sys

def progressBar(count,total, status=''):
    barLength = 60
    filledLength = int(round(barLength * count / float(total)))

    percent = round(100.0 * count / float(total),1)
    bar = '='*filledLength + '-'*(barLength-filledLength)

    sys.stdout.write(f'\rloading progress : [{bar}] {percent}% {status}    ')
    sys.stdout.flush()

def createModel(shape=(204,146,1)):
    model = models.Sequential()
    model.add(layers.Conv2D(32,(3,3),activation='relu',input_shape=shape))
    model.add(layers.MaxPool2D((2,2)))
    model.add(layers.Dropout(0.5))

    model.add(layers.Conv2D(64,(3,3),activation='relu'))
    model.add(layers.MaxPool2D((2,2)))
    model.add(layers.Dropout(0.5))

    model.add(layers.Conv2D(128,(3,3),activation='relu'))
    model.add(layers.MaxPool2D((2,2)))
    model.add(layers.Dropout(0.5))

    model.add(layers.Flatten())
    model.add(layers.Dense(256,activation='relu'))
    model.add(layers.Dense(2,activation='relu'))
    model.summary()
    model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
    return model

def loadData(filepath=''):
    train = []
    labels = []
    labelClasses = {}
    i = 0
    for item in os.listdir(filepath):
        labelClasses[i] = item
        _filepath = filepath+ '/' + item + '/'
        j = 0
        for imgPath in os.listdir(_filepath):
            progressBar(j,len(os.listdir(_filepath)),status=f'{item}')
            if int(imgPath.split('.')[0].split('-')[-1]) < 5:
                _img = Image.open(_filepath+imgPath).convert('L')
                train.append(np.array(_img)/255.0)
                labels.append(i)
                del _img
            j += 1
        i += 1

    shuffler = np.random.permutation(len(train))
    
    train = np.array(train)
    labels = np.array(labels)

    train = train[shuffler]
    labels = labels[shuffler]

    train = train.reshape([-1,146,204,1])
    return train, labels, labelClasses

def getData(save=False,filepath='',setRecognitionData='SetDetectionData'):
    for folder in os.listdir(setRecognitionData):
        for i in range(1,300):
            for cardImg in folder:
                pass



def visualizeLoss(history):
    lossLine = plt.plot([i for i in range(1,len(history.history['loss'])+1)],history.history['loss'],'b')
    valLossLine = plt.plot([i for i in range(1,len(history.history['val_loss'])+1)],history.history['val_loss'],'g')
    plt.setp(lossLine, label='loss') 
    plt.setp(valLossLine, label='validation loss')
    plt.legend(loc='upper right')
    plt.show()

def visualizeAcc(history):
    accLine = plt.plot([i for i in range(1,len(history.history['accuracy'])+1)],history.history['accuracy'],'b')
    valAccLine = plt.plot([i for i in range(1,len(history.history['val_accuracy'])+1)],history.history['val_accuracy'],'g')
    plt.setp(accLine, label='accuracy') 
    plt.setp(valAccLine, label='validation accuracy')
    plt.legend(loc='lower right')
    plt.show()

def trainModel(model, train, labels, epochs=10):
    history = model.fit(x=train,y=labels,epochs=epochs,validation_split=0.1)
    visualizeLoss(history)
    visualizeAcc(history)
    return history

def loadModel(filepath=''):
    model = models.load_model(filepath)
    return model

def loadLabelClasses(filepath=''):
    labelClasses = {}
    i = 0

    for item in os.listdir(filepath):
        labelClasses[i] = item
        i += 1

    return labelClasses

if __name__ == '__main__':
    CardRecognitionModel = createModel()
    filePath = 'CardDetectionData'
    if '-train' in sys.argv:
        train, labels, labelClasses = loadData(filepath='CardDetectionData')
        history = trainModel(CardRecognitionModel, train, labels)
    elif '-load' in sys.argv:
        CardRecognitionModel = loadModel()
    elif '-download' in sys.argv:
        if not os.path.exists(filePath):
            os.mkdir(filePath)
            getData(save=True, filepath=filePath)

    