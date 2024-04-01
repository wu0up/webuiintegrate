import cv2, os, numpy as np
from deepface import DeepFace


def crop_face(inputfile, fileName):
    outputFile = r"C:\Users\PJ-Lin\Documents\webuilight\testImg"
    fileName = inputfile.split("\\")[-1]
    im = cv2.imread(inputfile)

    result = DeepFace.extract_faces(im,
                                    detector_backend="retinaface",
                                    enforce_detection=False)

    img_crop = []
    for res in result:
        facial_area = res["facial_area"]
        cv2.rectangle(im, (facial_area["x"], facial_area["y"]),
                      (facial_area["x"] + facial_area["w"],
                       facial_area["y"] + facial_area["h"]), (0, 255, 0), 1)
        img_crop.append(
            im[facial_area["y"]:facial_area["y"] + facial_area["h"],
               facial_area["x"]:facial_area["x"] + facial_area["w"]])

    images = {}

    for counter, cropped in enumerate(img_crop):
        name = f"{fileName}_{counter}.png"
        if name not in images:
            images[name] = img_crop
            # cv2.imshow(str(counter), cropped)

            cv2.imwrite(outputFile + "\\" + name, cropped)
            cv2.waitKey(0)

    return images
