import cv2, os, numpy as np
from deepface import DeepFace


def crop_face(inputfile, fileName):
    outputFile = os.path.dirname(inputfile)
    new_width = 256
    new_height = 256
    im = cv2.imread(inputfile)

    result = DeepFace.extract_faces(im,
                                    detector_backend="retinaface",
                                    enforce_detection=False)

    enlarged_faces = {}

    for idx, res in enumerate(result):
        facial_area = res["facial_area"]
        cv2.rectangle(im, (facial_area["x"], facial_area["y"]),
                      (facial_area["x"] + facial_area["w"],
                       facial_area["y"] + facial_area["h"]), (0, 255, 0), 1)

        # 放大臉部區域
        enlarged_face = cv2.resize(
            im[facial_area["y"]:facial_area["y"] + facial_area["h"],
               facial_area["x"]:facial_area["x"] + facial_area["w"]],
            (new_width, new_height))  # 設定新的寬度和高度

        name = f"{fileName}_{idx}.png"
        outputpath = os.path.join(outputFile, name)
        cv2.imwrite(outputpath, enlarged_face)

        enlarged_faces[name] = outputpath

    return enlarged_faces
