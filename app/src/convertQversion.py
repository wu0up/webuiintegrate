import json
import requests
import io, os, sys

import base64
from PIL import Image
import cv2
from PIL import Image, PngImagePlugin
from datetime import datetime

from app.src import normalize_path, encode_image, age_detection, gender_modified
from app.src import cropFace

from config import configs as p

# tool = api.Api()
url = p.WEBUI_URL

# 如果拍攝的是物體，或多個人


def convertQversion(image, gender, name, save_path):

    # 如果沒有檔案，或檔案不是png
    # img = cv2.imread(path)
    # retval, bytes = encode_image(img, file_path)
    # if retval == False:
    #     return []
    # 如果不是人，race=False
    age, race = age_detection(image)
    if race == False:
        return []
    # 確認年齡
    people_describe = gender_modified(age, gender, race)
    prompt = p.prompt1 + people_describe + p.prompt2
    # encoded_image = base64.b64encode(bytes).decode('utf-8')
    body = p.qface_config
    body["init_images"] = [image]
    body["prompt"] = prompt
    print(f'send response, {people_describe}')
    # response = requests.post(url=f'{url}/sdapi/v1/img2img', json=body)
    # r = response.json()
    # image = Image.open(
    #     io.BytesIO(base64.b64decode(r['images'][0].split(",", 1)[0])))
    image = Image.open(image)
    # name = path.split("/")[-1]
    name = name
    current_datetime = datetime.now().strftime("%Y-%m-%d_")
    file_path = save_path + current_datetime + name + "_imgtoimg" + age + ".png"
    image.save(file_path)
    #    pnginfo=PI)
    image.show()

    return file_path
