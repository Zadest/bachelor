#! /usr/bin/env python3
# -*- coding: utf8 -*-

__version__ = "0.1"

import os, sys, json, csv
import requests
import logging
from PIL import Image
from io import BytesIO

images = []

def init():
    logging.basicConfig(filename='./oberon.log',level=logging.DEBUG,format='[%(asctime)s][%(levelname)s]: %(message)s')
    logging.info(f'started : Oberon v{__version__}')
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

init()
getImagesFromScryfall()