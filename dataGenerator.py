import requests
import json
from time import sleep
from io import BytesIO
from PIL import Image

def getImgsForSet(setCode):
    try:
        response = requests.get('https://api.scryfall.com/sets/'+setCode)
        data = json.load(BytesIO(response.content))['data']
        cardCount = data['card_count']
    except Exception as e:
        print(e)
        print('Unable to get set information')
