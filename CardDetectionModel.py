import numpy as np

from PIL import Image
from keras import models
from keras import layers, losses, preprocessing

import random
import os
import sys

def createModel(shape=(146, 204, 1)):
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=shape))
    model.add(layers.MaxPool2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.MaxPool2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.MaxPool2D((2, 2)))
    model.add(layers.Dropout(0.5))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation="relu"))
    model.add(layers.Dense(2, activation="sigmoid"))
    model.summary()
    model.compile(
        optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )
    return model

def loadData(filepath=""):
    train = []
    labels = []
    labelClasses = {}
    i = 0
    for item in os.listdir(filepath):
        labelClasses[i] = item
        _filepath = filepath + "/" + item + "/"
        for imgPath in os.listdir(_filepath):
            _img = Image.open(_filepath + imgPath).convert("L")
            train.append(np.array(_img) / 255.0)
            labels.append(i)
            del _img
        i += 1
    shuffler = np.random.permutation(len(train))
    train = np.array(train)
    labels = np.array(labels)
    train = train[shuffler]
    labels = labels[shuffler]
    train = train.reshape([-1, 146, 204, 1])
    return train, labels, labelClasses

def trainModel(model, train, labels, epochs=10):
    history = model.fit(x=train, y=labels, epochs=epochs, validation_split=0.1)
    return model, history

def loadModel(filepath=""):
    model = models.load_model(filepath)
    return model

def loadLabelClasses(filepath=""):
    labelClasses = {}
    i = 0
    for item in os.listdir(filepath):
        labelClasses[i] = item
        i += 1
    return labelClasses

if __name__ == "__main__":
    CardDetectionModel = createModel()
    filePath = "CardDetectionData"
    if "-train" in sys.argv:
        train, labels, labelClasses = loadData(filepath="CardDetectionData")
        CardDetectionModel, history = trainModel(CardDetectionModel, train, labels)
        CardDetectionModel.save("CardDetectionModel")
    elif "-load" in sys.argv:
        CardDetectionModel = loadModel()
