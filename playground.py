import os
from config import filePath,classes

from keras import models, layers, losses
import cv2
import numpy as np
import random
from PIL import Image


data = os.listdir(filePath)
objects = {}

for item in data:
    number = item.split('.')[0].split('-')[-1]
    if(item.split('.')[-1] == 'jpg' and item.split('-')[0] in classes.values()):
        if number in objects:
            objects[number].append(item)
        elif int(number) < 300:
            objects[number] = [item]
        else:
            pass
    else:
        continue

model = models.Sequential() 
model.add(layers.Conv2D(32, 3,activation='relu', input_shape=(146,204,1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(300))
model.summary()

model.compile(optimizer='adam',
        loss=losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'])
        
train, train_labels = [],[]
test, test_labels = [],[]

for key in objects:
    print(key)
    temp = []
    for imgPath in objects[key]:
        npImg = cv2.imread(filePath+imgPath,0) / 255.0
        temp = temp + [npImg]
    random.shuffle(temp)
    '''
    train = train + temp[:int(len(temp)*0.75)]
    train_labels = train_labels + [int(key)]*int(len(temp)*0.75)
    '''
    train = train + temp
    train_labels = train_labels + [int(key)]*len(temp)
    '''
    test = test + temp[int(len(temp)*0.75):]
    test_labels = test_labels + [int(key)]*(len(temp)-int(len(temp)*0.75))
    '''
    del temp

train, train_labels = np.array(train).reshape([-1,146,204,1]),np.array(train_labels)
test, test_labels = np.array(test).reshape([-1,146,204,1]),np.array(test_labels)

print('lets go')

history = model.fit(x=train,y=train_labels,epochs=50,shuffle=True)