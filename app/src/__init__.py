import os, cv2, logging
from deepface import DeepFace
from config import configs as p


def normalize_path(input_path):
    # 将反斜杠替换为正斜杠（Windows和Linux都支持）
    input_path = input_path.replace('\\', '/')

    # 使用os.path.normpath()来规范化路径
    normalized_path = os.path.normpath(input_path)

    return normalized_path


def encode_image(img, file_path):
    # 获取文件扩展名
    _, file_ext = os.path.splitext(file_path)
    # 根据文件扩展名选择图像编码格式
    if file_ext.lower() == '.jpg':
        retval, bytes = cv2.imencode('.jpg', img)
    elif file_ext.lower() == '.png':
        retval, bytes = cv2.imencode('.png', img)
    else:
        # 其他未知格式，默认使用PNG格式
        return False, False
    return retval, bytes


def age_detection(img):
    try:
        obj = DeepFace.analyze(img, actions=['age', 'race'])
        age = obj[0].get("age")
        race = obj[0].get("dominant_race")
        return str(age), race
    except Exception as e:
        logging.error(f"Age_detection error:{e}")
        return str(50), False


# async def convertImg(jsonbody):
#     url = p.WEBUI_URL + "/sdapi/v1/img2img"
#     # response = requests.post(url=f'{url}/sdapi/v1/img2img', json=body)
#     response = await requestsApi("POST", url=url, body=json)
#     # print(f'r:{r}')
#     for i in response['images']:

#         image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
#         name = str(image)[-13:-1]

#         current_datetime = datetime.now()
#         current_datetime_str = current_datetime.strftime("%Y-%m-%d_")

#         image.save(save_path + current_datetime_str + name + "_imgtoimg" +
#                    age + ".png")
#         #    pnginfo=PI)
#         image.show()
#     return image


def gender_modified(age, gender, race):
    age = int(age)
    if age < 18 and gender == "man":
        gender = "boy"
    elif age < 18 and gender == "woman":
        gender = "girl"
    people_describe = f"{age} years old {gender}, {race},"
    return people_describe
