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
