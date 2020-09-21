from PIL import Image
import os
import logging
import random
import datetime

from config import filePath, logPath

nfilePath = 'E:\\Python\\Bachelor\\2\\'
backgrounds = []
cards = []

def showAll(imgs):
    for i in imgs:
        i.show()

def generateDataset():
    # Vielleicht random Größe der testbilder?
    size = random.randint(300,650), random.randint(300,650)
    resizeFaktor = random.uniform(0.95,1.40)
    logging.info('> generator initiated')
    newImg = None
    if random.randint(0,2) == 2:
        # two cards in one image
        i = random.randint(0,len(cards))
        img1 = Image.open(filePath+cards.pop(i))
        img1 = img1.resize((int(img1.size[0]*resizeFaktor),int(img1.size[1]*resizeFaktor)))
        newImg1 = img1.convert('RGBA').rotate(random.randint(-15,15),expand=1)
        w1, h1 = newImg1.size
        #
        j = random.randint(0,len(cards))
        img2 = Image.open(filePath+cards.pop(j))
        newImg2 = img2.convert('RGBA').rotate(random.randint(-15,15),expand=1)
        w2, h2 = newImg1.size
        #
        k = random.randint(0,len(backgrounds)-1)
        newImg = Image.open(nfilePath+backgrounds[k])
        width, height = newImg.size
        x,y = random.randint(0,width-250),random.randint(0,height-250)
        newImg = newImg.crop((x,y,x+250,y+250))
        newImg = newImg.resize(size)
        width, height = newImg.size
        #
        startPixelX1 = random.randint(0,width-w1)
        startPixelX2 = random.randint(0,width-w2)
        startPixelY1 = random.randint(0,height-h1)
        startPixelY2 = random.randint(0,height-h2)
        #
        newImg.paste(newImg1,(startPixelX1,startPixelY1),newImg1)
        newImg.paste(newImg2,(startPixelX2,startPixelY2),newImg2)
        # 
        pass
    else:
        #
        i = random.randint(0,len(cards))
        img1 = Image.open(filePath+cards.pop(i))
        img1 = img1.resize((int(img1.size[0]*resizeFaktor),int(img1.size[1]*resizeFaktor)))
        newImg1 = img1.convert('RGBA').rotate(random.randint(-15,15),expand=1)
        w1, h1 = newImg1.size
        
        k = random.randint(0,len(backgrounds)-1)
        newImg = Image.open(nfilePath+backgrounds[k])
        width, height = newImg.size
        x,y = random.randint(0,width-250),random.randint(0,height-250)
        newImg = newImg.crop((x,y,x+250,y+250))
        newImg = newImg.resize(size)
        width, height = newImg.size

        startPixelX1 = random.randint(0,width-w1)
        startPixelY1 = random.randint(0,height-h1)
        newImg.paste(newImg1,(startPixelX1,startPixelY1),newImg1)
        # one card in one image
        pass
    return newImg


if __name__== "__main__":
    logging.basicConfig(format='%(asctime)s [%(levelname)s] : %(message)s',level=logging.INFO)
    logging.info('> helper')
    
    backgrounds = os.listdir(nfilePath)
    cards = os.listdir(filePath)
    
    newImages = []
    for i in range(0,10):
        newImages.append(generateDataset())
    index = 0
    for element in newImages:
        element.convert('RGB').save('E:\\Python\\Bachelor\\3\\img\\'+str(index)+'.jpg')
        index += 1