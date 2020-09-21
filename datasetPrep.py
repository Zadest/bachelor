import numpy as np
from config import filePath
import json
import os
import random
from PIL import Image, ImageFilter

#classes = {0:'grn',1:'rna', 2:'war', 3:'m20', 4:'eld', 5:'thb', 6:'iko', 7:'m21'}

label_classes = {}

def writeLabels():
    with open('E:\\Python\\Bachelor\\setLabels.json','w') as f:
        json.dump(label_classes,f)

def dataGenerator():
    _filePath = filePath
    for folder in os.listdir(_filePath):
        for imgFile in os.listdir(_filePath+folder+'\\'):
            for i in range(0,10):
                img = Image.open(_filePath+folder+'\\'+imgFile)
                img = img.rotate(random.uniform(-5.0,5.0),expand=True)
                img = img.resize((146,204))
                img.save(_filePath+folder+'\\'+imgFile.split('.')[0]+'-'+str(i)+'.jpg')
                del img

def dataLoader():
    _filePath = filePath
    labelIndex = 0
    labels = []
    train = []
    for folder in os.listdir(_filePath):
        label_classes[labelIndex] = folder
        for imgFile in os.listdir(_filePath+folder+'\\'):
            _tempImg = Image.open(_filePath+folder+'\\'+imgFile).convert('L')
            _tempArray = np.array(_tempImg) * 1./255
            train.append(_tempArray)
            del _tempArray, _tempImg
            labels.append(labelIndex)
        labelIndex += 1

    train = np.array(train)
    labels = np.array(labels)

    shuffler = np.random.permutation(len(train))
    training = train[shuffler]
    training_label = labels[shuffler]
    writeLabels()
    return training, training_label
    
if __name__ == '__main__':
    #dataLoader()
    dataGenerator()