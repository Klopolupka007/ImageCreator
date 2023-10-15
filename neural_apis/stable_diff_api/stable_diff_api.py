import asyncio

import base64
from io import BytesIO
import uvicorn
from fastapi import FastAPI, Request

from models_loader import get_all_models
from PIL import Image
#from fastapi.middleware.cors import CORSMiddleware
#import nest_asyncio
#from pyngrok import ngrok


all_sd_models = get_all_models()

STANDARD_IMAGE_SIZE = (512, 512)
CHANNEL_BANNER_IMAGE_SIZE = (768, 512)


stable_diff_app = FastAPI()


@stable_diff_app.post('/generate_image_by_prompt')
async def generate_image_by_prompt(request: Request):
    
    base_model = all_sd_models["base_model"]
    
    request_body = await request.json()
    
    prompt = request_body["prompt"]
    lora_name = request_body["lora_name"]
    task = request_body["task"]
    
    if task == "banner":
        height, width = 512, 1304
    elif task == "thumbnail":
        height, width = 512, 768
    elif task == "avatar":
        height, width = 512, 512
    
    
    generated_image = base_model.generate_image(
        prompt,
        lora_name,
        height=height,
        width=width
    )
    
    generated_image = image_to_base64(generated_image)
    
    return {"generated_image": generated_image}


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    return image_base64


@stable_diff_app.post('/generate_image_controlnet_pose')
async def generate_image_controlnet_pose(request: Request):
    
    request_body = await request.json()
    
    prompt = request_body["prompt"]
    lora_name = request_body["lora_name"]
    pose_image = request_body["pose_image"]
    task = request_body["task"]
    
    pose_image = b64_to_pil(pose_image)
    
    if task == "banner":
        height, width = 512, 1304
    elif task == "avatar":
        height, width = 512, 512
    
    pose_model = all_sd_models["pose_model"]

    generated_image = pose_model.generate_image(
        pose_image,
        prompt,
        lora_filename=lora_name,
        height=height,
        width=width
    )
    
    generated_image = image_to_base64(generated_image)
    
    return {"generated_image": generated_image}


def b64_to_pil(img_b64):
    decoded_image = base64.b64decode(img_b64)
    image_PIL = Image.open(BytesIO(decoded_image))
    
    return image_PIL


@stable_diff_app.post('/generate_image_controlnet_face')
async def generate_image_controlnet_face(request: Request):
    
    request_body = await request.json()
    
    prompt = request_body["prompt"]
    lora_name = request_body["lora_name"]
    pose_image = request_body["face_pose_image"]
    task = request_body["task"]
    
    pose_image = b64_to_pil(pose_image)
    
    if task == "banner":
        height, width = 512, 1304
    elif task == "avatar":
        height, width = 512, 512
    
    pose_model = all_sd_models["face_model"]
    
    generated_image = pose_model.generate_image(
        pose_image,
        prompt,
        lora_filename=lora_name,
        height=height,
        width=width
    )
    
    generated_image = image_to_base64(generated_image)
    
    return {"generated_image": generated_image}


@stable_diff_app.post('/generate_image_inpaint')
async def generate_image_inpaint(request: Request):

    request_body = await request.json()

    prompt = request_body["prompt"]
    lora_name = request_body["lora_name"]
    orig_image = request_body["orig_image"]
    mask_image = request_body["mask_image"]
    task = request_body["task"]
    
    orig_image = b64_to_pil(orig_image)
    mask_image = b64_to_pil(mask_image)
    
    if task == "banner":
        height, width = 512, 1304
    elif task == "avatar":
        height, width = 512, 512
    
    pose_model = all_sd_models["inpaint_model"]
    
    generated_image = pose_model.generate_image(
        orig_image,
        mask_image,
        prompt,
        lora_name,
        height=height,
        width=width
    )
    
    generated_image = image_to_base64(generated_image)
    
    return {"generated_image": generated_image}


'''stable_diff_app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)'''

async def main():
    config = uvicorn.Config(
        "stable_diff_api:stable_diff_app",
        port=8500,
        log_level="info",
        workers=6
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())