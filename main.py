#import cv2 as cv
#import numpy as np
#from PIL import Image

# ------------------------------

from config import filePath, logPath, verbose, classes

# ------------------------------

import os
import sys
import logging
import json
import requests
import datetime
from time import sleep
from io import BytesIO
from PIL import Image

#################
###
#
# Initiation - Funktion, die gewährleiste, dass die benötigte Ordnerstruktur vorhanden ist.
#
###
#################
def __init__():
    if not os.path.exists(filePath):
        os.mkdir(filePath)
    if not os.path.exists(logPath):
        os.mkdir(logPath)
    logging.basicConfig(filename=logPath+datetime.datetime.now().strftime('%Y-%m-%d')+'.log',level=logging.INFO,format='%(asctime)s [%(levelname)s] : %(message)s')
    logging.info('Bachelor-Arbeits-Programm initializiert.')

#################
###
#
# Loesche leere Sets und Sets, deren Setcode mehr als drei Zeichen beinhaltet (Tokens/Promos/Specials)
#
###
#################
def __fixProblemDownload__(sets):
    tempSets = {}
    for key in sets:
        if sets[key] != 0 and len(key) <= 3: 
            tempSets[key] = sets[key]
    return tempSets

#################
###
#
#
#
###
#################
def __getSetsFromScryfall__():
    sets = {}
    try:
        response = requests.get('https://api.scryfall.com/sets')
    except Exception as e:
        print(e)
        logging.error(e)
        return False, None
    data = json.load(BytesIO(response.content))
    for Set in data['data']:
        if datetime.datetime.strptime(Set['released_at'],'%Y-%m-%d').year > 1997 and int(Set['card_count']) > 0 and Set['code'] != 'cmr':
            sets[Set['code']] = Set['card_count']
    return True, sets

#################
###
#
#
#
###
#################
def __getImagesForSet__(setCode,count):
    _filePath=filePath+setCode+'\\'
    os.mkdir(_filePath)
    
    for x in range(1,count):
        sleep(0.1)
        try:
            response = requests.get(f'https://api.scryfall.com/cards/{setCode}/{x}')
        except Exception as e:
            print(e)
            logging.error(e)
            return False
        data = json.load(BytesIO(response.content))
        if 'image_uris' in data.keys():
            response = requests.get(data['image_uris']['normal'])
            try:
                img = Image.open(BytesIO(response.content))
                img.save(_filePath + setCode +'-'+str(x)+'.jpg')
                if verbose:
                    print(f'{setCode} ID : {str(x)}')
                    logging.info(f'{setCode} ID : {str(x)}')
            except:
                continue
        else:
            if verbose:
                logging.info(f'{setCode} hat keine Bilddateien zu ID : {str(x)}')
    return True

#################
###
#
#
#
###
#################
def __createFalseData__():
    return True

#################
###
#
#
#
###
#################
if __name__ == "__main__":
    for setCode in classes.values():
        __getImagesForSet__(setCode,300)
    """__init__()
    if len(sys.argv) > 1:
        if "-v" in sys.argv:
            verbose = False
    done, sets = __getSetsFromScryfall__()
    #sets = __fixProblemDownload__(sets)
    with open(filePath+'data.dat','w') as f:
        f.write(json.dumps(sets))
    sofar = 0
    total = sum(sets.values())
    if os.path.exists(filePath+'done.dat'):
        with open(filePath+'done.dat','r') as f:
            done = json.load(f)
        for key in done['sets']:
            if key in sets:
                sets.pop(key,None)
    else:
        done = {}
    
    print(sets)

    for Set in sets:
        deltaTime = datetime.datetime.now()
        sleep(1)
        result = __getImagesForSet__(Set,sets[Set])
        if result:
            pass
            #done['sets'].append(Set)
        sofar += sets[Set]
        deltaTime = datetime.datetime.now() - deltaTime
        print(Set+' ; '+'% : '+str((sofar / total)*100)+' ; Cards / Total : '+str(sofar)+ ' / '+str(total)+' ; Time passed (seconds) : '+ str(deltaTime.seconds))
        logging.info(Set+' ; '+'% : '+str((sofar / total)*100)+' ; Cards / Total : '+str(sofar)+ ' / '+str(total)+' ; Time passed (seconds) : '+ str(deltaTime.seconds))
"""