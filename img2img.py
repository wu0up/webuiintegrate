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


def convertQversion(filepath, gender, fileName):
    outputFile = os.path.dirname(filepath)
    # 如果沒有檔案，或檔案不是png
    img = cv2.imread(filepath)
    retval, bytes = encode_image(img, filepath)
    if retval == False:
        return []
    age = [15, 30, 50]
    # 如果不是人，race=False
    # age, race = age_detection(filepath)
    # if race == False:
    #     return []
    # 確認年齡
    for a in age:
        people_describe = gender_modified(a, gender)
        prompt = p.prompt1 + people_describe + p.prompt2
        encoded_image = base64.b64encode(bytes).decode('utf-8')
        body = p.qface_config
        body["init_images"] = [encoded_image]
        body["prompt"] = prompt
        print(f'send response, {people_describe},fileName: {fileName}')
        response = requests.post(url=f'{url}/sdapi/v1/img2img', json=body)
        r = response.json()
        image = Image.open(
            io.BytesIO(base64.b64decode(r['images'][0].split(",", 1)[0])))
        name = fileName.split(".")[-1]
        # name = filePath.split("/")[-1]
        file_path = outputFile + name + "_imgtoimg" + age + ".png"
        image.save(file_path)
    #    pnginfo=PI)

    return file_path


if __name__ == "__main__":
    file_path = r"C:\Users\PJ-Lin\Documents\webuilight\testImg\manypeople2.jpg"
    path = normalize_path(file_path)
    name = file_path.split("\\")[-1]
    gender = "male"
    images = cropFace.crop_face(path, name)
    images_path = []
    for key, value in images.items():
        filePath = convertQversion(value, gender, key)
        images_path.append(filePath)
    print("images_path", images_path)
