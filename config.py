import platform
import datetime
import os
import json
#
#----------------------------------
#
verbose = True

__version__ = 0.3

classes = {}

if os.path.exists('E:\\Python\\Bachelor\\setLabels.json'):
    with open('E:\\Python\\Bachelor\\setLabels.json','r') as f:
        classes = json.load(f)
else:
    classes = {0:'grn', 1:'rna', 2:'war', 3:'m20', 4:'eld', 5:'thb', 6:'iko', 7:'m21'}
#
# ---------------------------------
# Operating System dependend Variables
#

if platform.system() == 'Windows':
    filePath = 'E:\\Python\\Bachelor\\data_NumberDetection\\'
    logPath = 'E:\\Python\\Bachelor\\logs\\'

else:
    filePath = '~/Python/Bachelor/1/'
    logPath = '~/Python/Bachelor/logs/'