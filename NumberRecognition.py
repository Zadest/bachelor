import os
import sys

from io import BytesIO
import json
import requests
from time import sleep

import cv2 as cv
import numpy as np
from PIL import Image
from keras import models
from keras import layers, losses, preprocessing

import matplotlib.pyplot as plt

import random

import tensorflow as tf
import random as python_random


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

    model.add(layers.Conv2D(64,(3,3),activation='relu'))
    model.add(layers.MaxPool2D((2,2)))
    model.add(layers.Dropout(0.5))

    model.add(layers.Flatten())
    model.add(layers.Dense(64,activation='relu'))
    model.add(layers.Dense(300))
    model.summary()
    model.compile(optimizer='adam',loss=losses.SparseCategoricalCrossentropy(from_logits=True),metrics=['accuracy'])
    return model

def loadData(filepath=''):
    train = []
    labels = []
    labelClasses = {}
    i = 0
    for folder in os.listdir(filepath):
        labelClasses[i] = folder
        _filepath = filepath+ '/' + folder + '/'
        j = 0
        for imgPath in os.listdir(_filepath):
            progressBar(j,len(os.listdir(_filepath)),status=f'{folder}')
            _img = Image.open(_filepath+imgPath).convert('L')
            _temp = np.array(_img) * 1./255
            if i == 0 and j == 0:
                plt.imshow(np.array(_img))
                plt.show()
            train.append(_temp)
            labels.append(i)
            del _img, _temp
            j += 1
        i += 1
        print('')

    
    
    train = np.array(train)
    labels = np.array(labels)

    shuffler = np.random.permutation(len(train))

    train = train[shuffler]
    labels = labels[shuffler]
    
    train = train.reshape([-1,204,146,1])
    return train, labels, labelClasses

def getData(save=False,filepath='NumberDetectionData',setRecognitionData='SetDetectionData'):
    labelClasses = {}
    for folder in os.listdir(setRecognitionData):
        for cardImgName in os.listdir(setRecognitionData+'/'+folder):
            label = cardImgName.split('.')[0].split('-')[1]
            if label in labelClasses:
                _img = Image.open(setRecognitionData+'/'+folder+'/'+cardImgName)
                _img.save(filepath+'/'+str(label)+'/'+cardImgName)
            else:
                labelClasses[label] = label
                os.mkdir(filepath+'/'+str(label))
                _img = Image.open(setRecognitionData+'/'+folder+'/'+cardImgName)
                _img.save(filepath+'/'+str(label)+'/'+cardImgName)


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

def trainModel(model, train, labels, epochs=5):
    np.random.seed(2710)
    python_random.seed(2710)
    tf.random.set_seed(2710)
    plt.imshow(train[0])
    plt.ylabel(labels[0])
    history = model.fit(x=train,y=labels,epochs=epochs,validation_split=0.1)
    visualizeLoss(history)
    visualizeAcc(history)
    return history

def loadModel(filepath='NumberRecognitionModelSave'):
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
    NumberRecognitionModel = createModel()
    filePath = 'NumberDetectionData'
    if '-train' in sys.argv:
        train, labels, labelClasses = loadData(filepath='NumberDetectionData')
        history = trainModel(NumberRecognitionModel, train, labels,epochs=50)
    elif '-load' in sys.argv:
        NumberRecognitionModel = loadModel()
    elif '-setup' in sys.argv:
        if not os.path.exists(filePath):
            os.mkdir(filePath)
        getData(save=True, filepath=filePath)
