import os
import sys
from io import BytesIO
import json
import requests
from time import sleep
from PIL import Image
import random

def progressBar(count, total, status=""):
    barLength = 60
    filledLength = int(round(barLength * count / float(total)))
    percent = round(100.0 * count / float(total), 1)
    bar = "=" * filledLength + "-" * (barLength - filledLength)
    sys.stdout.write(f"\rloading progress : [{bar}] {percent}% {status}    ")
    sys.stdout.flush()

def generateNegativ():
    imgs = [
        Image.open("ImagesWithoutCards/" + imgPath)
        for imgPath in os.listdir("ImagesWithoutCards")
    ]
    counter = len(os.listdir("CardDetectionData/other/"))
    for img in imgs:
        width, height = img.size
        for i in range(0, width - 146, int((width - 146) * 0.05)):
            for j in range(0, height - 204, int((height - 204) * 0.075)):
                temp = img.crop((i, j, i + 146, j + 204)).convert("L")
                temp.save("CardDetectionData/other/" + str(counter) + ".jpg")
                counter += 1
                del temp

def pickRandom():
    files = []
    for folder in os.listdir("SetDetectionData"):
        files += os.listdir("SetDetectionData/" + folder)

    for i in range(0, 10001):
        temp = files.pop(random.randint(0, len(files) - 1))
        _filepath = "SetDetectionData/" + temp.split("-")[0] + "/"
        temp = Image.open(_filepath + temp)
        temp.save("CardDetectionData/card/" + str(i) + ".jpg")
        del temp

def getData(save=True, filepath=""):
    labelClasses = {
        0: "grn",
        1: "rna",
        2: "war",
        3: "m20",
        4: "eld",
        5: "thb",
        6: "iko",
        7: "m21",
    }
    _filepath = filepath
    for i in range(8):
        filepath = _filepath
        if save:
            filepath = _filepath + "/" + labelClasses[i]
            if not os.path.exists(filepath):
                os.mkdir(filepath)
        print(i)
        sleep(1.0)
        try:
            response = requests.get("https://api.scryfall.com/sets/" + labelClasses[i])
            data = json.load(BytesIO(response.content))
            cardCount = data["card_count"]
            for j in range(1, cardCount + 1):
                progressBar(j, cardCount, status=f"{labelClasses[i]}")
                try:
                    response = requests.get(
                        f"https://api.scryfall.com/cards/{labelClasses[i]}/{j}"
                    )
                    cardData = json.load(BytesIO(response.content))
                    if "image_uris" in cardData.keys():
                        try:
                            response = requests.get(cardData["image_uris"]["small"])
                            _img = Image.open(BytesIO(response.content))
                            if save:
                                _img.save(filepath + f"/{labelClasses[i]}-{j}.jpg")
                            for k in range(0, 10):
                                _tempImg = _img.rotate(
                                    random.uniform(-5, 5), expand=True
                                ).resize((146, 204))
                                if save:
                                    _tempImg.save(
                                        filepath + f"/{labelClasses[i]}-{j}-{k}.jpg"
                                    )
                        except Exception as e:
                            print(e)
                            print("fehler 3")
                except Exception as e:
                    print("fehler 2")
                    print(e)
        except Exception as e:
            print("fehler 1")
            print(e)

def setupFolder():
    setLabels = {
        0: "grn",
        1: "rna",
        2: "war",
        3: "m20",
        4: "eld",
        5: "thb",
        6: "iko",
        7: "m21",
    }

    if not os.path.exists("SetDetectionData"):
        os.mkdir("SetDetectionData")
    if not os.path.exists("CardDetectionData"):
        os.mkdir("CardDetectionData")
    if not os.path.exists("NumberDetectionData"):
        os.mkdir("NumberDetectionData")

    NumberDetectionDataList = [i for i in range(1, 300)]
    for subfolder in NumberDetectionDataList:
        if not os.path.exists("NumberDetectionData" + "/" + str(subfolder)):
            os.mkdir("NumberDetectionData" + "/" + str(subfolder))

    if not os.path.exists("CardDetectionData" + "/" + "card"):
        os.mkdir("CardDetectionData" + "/" + "card")
    if not os.path.exists("CardDetectionData" + "/" + "other"):
        os.mkdir("CardDetectionData" + "/" + "other")

    for subfolder in setLabels.values():
        if not os.path.exists("SetDetectionData" + "/" + subfolder):
            os.mkdir("SetDetectionData" + "/" + subfolder)

    # lade Bilddateien herunter
    print("downloading images")
    getData(filepath="SetDetectionData")

    labelClasses = {}
    filepath = "NumberDetectionData"
    for folder in os.listdir("SetDetectionData"):
        for cardImgName in os.listdir("SetDetectionData" + "/" + folder):
            label = cardImgName.split(".")[0].split("-")[1]
            if int(label) <= 299:
                if label in labelClasses:
                    _img = Image.open(
                        "SetDetectionData" + "/" + folder + "/" + cardImgName
                    )
                    _img.save(filepath + "/" + str(label) + "/" + cardImgName)
                else:
                    labelClasses[label] = label
                    _img = Image.open(
                        "SetDetectionData" + "/" + folder + "/" + cardImgName
                    )
                    _img.save(filepath + "/" + str(label) + "/" + cardImgName)
    generateNegativ()
    pickRandom()


if __name__ == "__main__":
    setupFolder()
