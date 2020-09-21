from PIL import Image
import os

_filePath = 'E:\\Python\\Bachelor\\data_NumberDetection\\'

for folder in os.listdir(_filePath):
    if folder != 'train': 
        for imgPath in os.listdir(_filePath+folder):
            index = imgPath.split('-')[1]

            if not os.path.exists(_filePath+'train\\'+str(index.split('.')[0])+'\\'):
                os.mkdir(_filePath+'train\\'+str(index.split('.')[0])+'\\')
            else:
                pass
            _tempImg = Image.open(_filePath+folder+'\\'+imgPath)
            _tempImg = _tempImg.resize((146,204))
            _tempImg.save(_filePath+'train\\'+str(index.split('.')[0])+'\\'+imgPath)
