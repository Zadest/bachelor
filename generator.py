from PIL import Image
import numpy as np
import config
import os
import random

from keras import Sequential
from keras import models, layers, losses, preprocessing

_filePath = 'E:\\Python\\Bachelor\\'

def constructCardDetectionModel():
    CardDetectionModel = models.Sequential() 
    CardDetectionModel.add(layers.Conv2D(2, 3,activation='relu', input_shape=(146,204,1)))
    CardDetectionModel.add(layers.MaxPooling2D((2, 2)))
    CardDetectionModel.add(layers.Conv2D(64, (3, 3), activation='relu'))
    CardDetectionModel.add(layers.MaxPooling2D((2, 2)))
    CardDetectionModel.add(layers.Conv2D(64, (3, 3), activation='relu'))
    CardDetectionModel.add(layers.Flatten())
    CardDetectionModel.add(layers.Dense(64, activation='sigmoid'))
    CardDetectionModel.add(layers.Dense(2))
    CardDetectionModel.summary()
    CardDetectionModel.compile(optimizer='adam',
                                loss=losses.SparseCategoricalCrossentropy(from_logits=True),
                                metrics=['accuracy'])                                
    return CardDetectionModel

def trainModel():
    model = models.Sequential() 
    model.add(layers.Conv2D(2, 3,activation='relu', input_shape=(146,204,1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(2))
    model.summary()
    model.compile(optimizer='adam',
            loss=losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'])

    labelIndex = 0
    label_classes = {}
    labels = []
    train = []
    for folder in os.listdir(_filePath+'data\\train\\'):
        label_classes[labelIndex] = folder
        for imgFile in os.listdir(_filePath+'data\\train\\'+folder+'\\'):
            _tempImg = Image.open(_filePath+'data\\train\\'+folder+'\\'+imgFile).convert('L')
            _tempArray = np.array(_tempImg) * 1./255
            train.append(_tempArray)
            del _tempArray, _tempImg
            labels.append(labelIndex)
        labelIndex += 1

    train = np.array(train).reshape([-1,146,204,1])
    labels = np.array(labels)

    shuffler = np.random.permutation(len(train))

    train = train[shuffler]
    labels = labels[shuffler]

    history = model.fit(x=train, y=labels, epochs=5, validation_split=0.2)
    return model, history

def generateNegativ(imgs):
    counter = len(os.listdir(_filePath+'data\\train\\other\\'))
    for img in imgs:
        width, height = img.size
        for i in range(0,width-146,int((width-146)*0.05)):
            for j in range(0,height-204,int((height-204)*0.075)):
                temp = img.crop((i,j,i+146,j+204)).convert('L')
                temp.save(_filePath+'data\\train\\other\\'+str(counter)+'.jpg')
                counter += 1
                del temp

def pickRandom():
    files = os.listdir(config.filePath)
    counter = 0
    for i in range(0,10001):
        temp = files.pop(random.randint(0,len(files)-1))
        temp = Image.open(config.filePath+temp)
        temp.save(_filePath+'data\\train\\card\\'+str(counter)+'.jpg')
        del temp
        counter += 1

if __name__ == '__main__':
    print('> Generator Suite Started <')
    """imgs = []
    for item in os.listdir(_filePath+'2\\'):
        imgs = imgs + [Image.open(_filePath+'2\\'+item)]
    generateNegativ(imgs)
    #pickRandom()"""
    model = models.load_model(_filePath+'CardDetectionModel.pb')
