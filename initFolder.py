#! /usr/bin/env python3
# -*- coding: utf8 -*-

__version__ = "0.1"

import os, sys, json, csv, glob
import requests
import logging
import numpy as np
import cv2 as cv
from PIL import Image
from io import BytesIO
from time import sleep

images = []

def setupFolders():
    done = True
    try:
        os.makedirs('./data/1/keys/')
    except Exception as e:
        logging.info(e)
        done = False
    try:
        os.makedirs('./data/2/keys/')
    except Exception as e:
        logging.info(e)
        done = False
    finally:
        return done

def init():
    logging.basicConfig(filename='./oberon.log',level=logging.DEBUG,format='[%(asctime)s][%(levelname)s]: %(message)s')
    logging.info(f'started : Oberon v{__version__}')
    print(f'started : Oberon v{__version__}')
    if not os.path.exists('./data/1/keys/') or not os.path.exists('./data/2/keys/'):
        setupFolders()
    

def getImagesFromScryfall():
    try:
        response = requests.get('https://api.scryfall.com/cards/')
    except Exception as e:
        logging.warning('unable to connect to scryfall')
        logging.warning(e)
        return False
    data = json.load(BytesIO(response.content))
    count = 0
    lastname = ''
    for card in data['data']:
        if 'image_uris' in card.keys() and card['name'] != lastname:
            print(card['name'])
            response = requests.get(card['image_uris']['large'])
            images.append(Image.open(BytesIO(response.content)))
            lastname = card['name']
            count += 1
    print(count)
    filepath = './data/1/'
    filetype = '.jpg'
    index = 0    
    for img in images:
        img.save(filepath+str(index)+filetype)
        index += 1
    return True

def getImagesNotMTG():
    try:
        img = Image.open('./data/2/RAW.jpg')
    except Exception as e:
        print(e)
        return False
    width, height = img.size
    filepath = './data/2/'
    filetype = '.jpg'
    index = 0
    for i in range(0,width-672,int(672/3)):
        for j in range(0,height-936,int(936/3)):
            temp = img.crop((i,j,i+672,j+936))
            temp.save(filepath+str(index)+filetype)
            del temp
            index += 1
    return True

if __name__ == '__main__':
    init()
    if len(sys.argv) > 1:
        if 'mtg-load' in sys.argv:
            getImagesFromScryfall()
        if 'false-load' in sys.argv:
            getImagesNotMTG()
        if 'test' in sys.argv:
            image = cv.imread('/home/moritz/dev/bachelor/data/1/130.jpg',0)
            edges = cv.Canny(image,100,200)
            cv.imshow('test',edges)
            cv.waitKey(0)
            cv.destroyAllWindows()
        if 'lol':
            cap = cv.VideoCapture(0)
            while(True):
                # Capture frame-by-frame
                ret, frame = cap.read()

                # Our operations on the frame come here
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                edges = cv.Canny(gray,30,150)
                # Display the resulting frame
                cv.imshow('gray',gray)
                cv.imshow('edges',edges)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break

            # When everything done, release the capture
            cap.release()
            cv.destroyAllWindows()
