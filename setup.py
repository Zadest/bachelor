#######################
##
## setup.py
##
## Von messer17
##
#######################
import platform
import os

_filePathData = ''
_filePathModel = ''
_filePathApp = ''

# Generiere Dateistruktur abhaengig vom OS
if platform.system() == 'Windows':
    # DataPath
    if not os.path.exists('.\\data\\'):
        os.mkdir('.\\data\\')
    if not os.path.exists('.\\data\\CardDetection\\'):
        os.mkdir('.\\data\\CardDetection\\')
    if not os.path.exists('.\\data\\SetDetection\\'):
        os.mkdir('.\\data\\SetDetection\\')
    if not os.path.exists('.\\data\\NumberDetection\\'):
        os.mkdir('.\\data\\NumberDetection\\')
    
    # ModelPath
    if not os.path.exists('.\\CNN\\'):
        os.mkdir('.\\CNN\\')
    if not os.path.exists('.\\CNN\\CardDetection\\'):
        os.mkdir('.\\CNN\\CardDetection\\')
    if not os.path.exists('.\\CNN\\SetDetection\\'):
        os.mkdir('.\\CNN\\SetDetection\\')
    if not os.path.exists('.\\CNN\\NumberDetection\\'):
        os.mkdir('.\\CNN\\NumberDetection\\')    

else:
    # DataPath
    if not os.path.exists('./data/'):
        os.mkdir('./data/')
    if not os.path.exists('./data/CardDetection/'):
        os.mkdir('./data/CardDetection/')
    if not os.path.exists('./data/SetDetection/'):
        os.mkdir('./data/SetDetection/')
    if not os.path.exists('./data/NumberDetection/'):
        os.mkdir('./data/NumberDetection/')
    
    # ModelPath
    if not os.path.exists('./CNN/'):
        os.mkdir('./CNN/')
    if not os.path.exists('./CNN/CardDetection/'):
        os.mkdir('./CNN/CardDetection/')
    if not os.path.exists('./CNN/SetDetection/'):
        os.mkdir('./CNN/SetDetection/')
    if not os.path.exists('./CNN/NumberDetection/'):
        os.mkdir('./CNN/NumberDetection/')
        
 