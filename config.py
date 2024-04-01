from pydantic import BaseSettings, Field
from functools import lru_cache
from typing import Optional
import logging, os

logger = logging.getLogger(__name__)


class Settings(BaseSettings):

    WEBUI_URL: Optional[str] = Field(None, env="WEBUI_URL")

    class Config:
        env_file = ".env"


class Config(Settings):

    os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = "python"
    if Settings().WEBUI_URL is None:
        WEBUI_URL = "https://stable-difussion:7860"

    prompt1 = "No wings, face lens,white background,reality,"
    prompt2 = "crown, brown eyes,  raditional clothing,gold embroidery,whole body,(stading:1.3),No base required, golden clothes,red clothes,bun hair ,Gorgeous headdress, <lora:mingStyle8:0.5>, <lora:Doorgods:0.3>"
    negative_prompt = "nsfw,ugly,bad_anatomy,bad_hands,extra_hands,missing_fingers,broken hand,more than two hands,well proportioned hands,more than two legs,unclear eyes,missing_arms,mutilated,extra limbs,extra legs,cloned face,fused fingers,extra_digit, fewer_digits,extra_digits,jpeg_artifacts,signature,watermark,username,blurry,large_breasts,worst_quality,low_quality,normal_quality,mirror image, Vague"
    batch_size = 1
    # save_path = "C:\\Users\\User\\Desktop\\API\\"
    image_pose = ""

    qface_config = {
        "override_settings": {
            "sd_model_checkpoint": "helloq3Q_helloq3V10c.safetensors",
            "sd_vae": "animevae.pt",
            "CLIP_stop_at_last_layers": 2,
        },

        # 基本参数
        "prompt": "",
        "negative_prompt": negative_prompt,
        "steps": 30,
        "sampler_name": "DPM++ SDE Karras",
        "width": 512,
        "height": 512,
        "batch_size": 3,
        "n_iter": 1,
        "seed": -1,
        "cfg_scale": 7,
        "CLIP_stop_at_last_layers": 2,
        "denoising_strength": 0.5,
        # "init_images": [encoded_image],
        "init_images": [],

        # 面部修复 face fix
        "restore_faces": False,

        #高清修复 highres fix
        # "enable_hr": True,
        # "denoising_strength": 0.4,
        # "hr_scale": 2,
        # "hr_upscaler": "Latent",
        "alwayson_scripts": {
            # "ControlNet":{
            #     "args": [
            #                 {
            #                     "enabled": True,
            #                     "module": "none",
            #                     "model": "canny",
            #                     "weight": 1.0,
            #                     "image": image_pose,
            #                     "resize_mode": 1,
            #                     "lowvram": False,
            #                     "processor_res": 64,
            #                     "threshold_a": 64,
            #                     "threshold_b": 64,
            #                     "guidance_start": 0.0,
            #                     "guidance_end": 1.0,
            #                     "control_mode": 0,
            #                     "pixel_perfect": False
            #                 }
            #             ]
            # },
            # "roop": {
            #     "source_image": r"C:\Users\User\Desktop\output333.png",
            #     "target_image": "",
            #     "face_index": [0],
            #     "scale": 1,
            #     "upscale_visibility": 1,
            #     "face_restorer": "None",
            #     "restorer_visibility": 1,
            #     "model": "inswapper_128.onnx"
            # }
        }
    }


@lru_cache()
def get_configs():
    configs = Config()
    logging.basicConfig(level=logging.INFO)
    config_vars = vars(configs)
    for key, value in config_vars.items():
        if key.isupper() and key not in (
                "ENSAAS_SERVICES", "OPENAI_API_KEY") and value is not None:
            logging.info(f"[ENV]  {key} ok ... : {value}")

    return configs


configs = get_configs()
