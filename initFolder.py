#! /usr/bin/env python3
# -*- coding: utf8 -*-

__version__ = "0.1"

import os, sys, json, csv
import requests
import logging
from PIL import Image
from io import BytesIO

def init():
    global logging.
    try:
        os.makedirs('./data/1/')
        os.makedirs('./data/2/')    
        return True
    except Exception as e:
        print(e)
        return False

init()
