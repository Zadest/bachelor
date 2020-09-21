from keras import models, layers, losses
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from datasetPrep import dataLoader, label_classes

#input_shape = (4, 146, 204, 3)

# Convolutional Layers

# Pooling Layers

model = models.Sequential() 
model.add(layers.Conv2D(32, 3,activation='relu', input_shape=(146,204,1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(8))
model.summary()
model.compile(optimizer='adam',
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'])


from config import filePath
import json
import os

from PIL import Image
# GRN, RNA, WAR, M20, ELD, THB, IKO, M21
def trainModel():
        size = (146,204)

        train_images, train_labels = dataLoader()
        train_images = np.reshape(train_images,[-1,146,204,1])

        history1 = model.fit(x=train_images,y=train_labels,epochs=5,validation_split=0.1)
#
if __name__ == '__main__':
        model = models.load_model('E:\\Python\\Bachelor\\')