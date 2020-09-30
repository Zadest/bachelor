import os
import sys

import numpy as np
from PIL import Image
from keras import models
from keras import layers, losses, preprocessing
import random
import tensorflow as tf
import random as python_random


def createModel(shape=(204, 146, 1)):
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
    model.add(layers.Dense(300))
    model.summary()
    model.compile(
        optimizer="adam",
        loss=losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )
    return model


def loadData(filepath=""):
    train = []
    labels = []
    labelClasses = {}
    i = 0
    for folder in os.listdir(filepath):
        labelClasses[i] = folder
        _filepath = filepath + "/" + folder + "/"
        for imgPath in os.listdir(_filepath):
            _img = Image.open(_filepath + imgPath).convert("L")
            _temp = np.array(_img) * 1.0 / 255
            train.append(_temp)
            labels.append(i)
            del _img, _temp
        i += 1

    train = np.array(train)
    labels = np.array(labels)
    shuffler = np.random.permutation(len(train))
    train = train[shuffler]
    labels = labels[shuffler]
    train = train.reshape([-1, 204, 146, 1])
    return train, labels, labelClasses


def trainModel(model, train, labels, epochs=5):
    np.random.seed(2710)
    python_random.seed(2710)
    tf.random.set_seed(2710)
    history = model.fit(x=train, y=labels, epochs=epochs, validation_split=0.1)
    return history


def loadModel(filepath="NumberRecognitionModelSave"):
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
    NumberDetectionModel = createModel()
    filePath = "NumberDetectionData"
    if "-train" in sys.argv:
        train, labels, labelClasses = loadData(filepath="NumberDetectionData")
        history = trainModel(NumberDetectionModel, train, labels, epochs=50)
    elif "-load" in sys.argv:
        NumberDetectionModel = loadModel()
