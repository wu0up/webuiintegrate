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


def convertQversion(image, gender, filePath):

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
    response = requests.post(url=f'{url}/sdapi/v1/img2img', json=body)
    r = response.json()
    image = Image.open(
        io.BytesIO(base64.b64decode(r['images'][0].split(",", 1)[0])))
    image.show()
    # image = Image.fromarray(image)
    # name = path.split("/")[-1]
    name = filePath.split("/")[-1]
    save_path = r"C:\Users\PJ-Lin\Documents\webuilight\testImg"
    current_datetime = datetime.now().strftime("%Y-%m-%d_")
    file_path = save_path + current_datetime + name + "_imgtoimg" + age + ".png"
    image.save(file_path)
    #    pnginfo=PI)

    return file_path


if __name__ == "__main__":
    file_path = r"C:\Users\PJ-Lin\Documents\webuilight\testImg\multiple.jpg"
    save_path = r"C:\Users\PJ-Lin\Documents\webuilight\testImg"
    path = normalize_path(file_path)
    name = file_path.split("\\")[-1]
    gender = "male"
    images = cropFace.crop_face(path, name)
    images_path = []
    for key, value in images.items():
        filePath = convertQversion(value[0], gender, key)
        images_path.append(filePath)
    print("images_path", images_path)
