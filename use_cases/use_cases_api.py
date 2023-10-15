import asyncio
import os
import sys

import requests
import uvicorn
from colorama import init
from fastapi import FastAPI, Request

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from common_tools.conf_logger import get_console_logger

init(convert=True)

logger = get_console_logger(__name__)


image_by_prompt_generator_url = "http://127.0.0.1:8500/generate_image_by_prompt"
upscale_image_url = "http://127.0.0.1:8300/upscale_image"
prompt_generator_url = "http://127.0.0.1:8400/generate_prompt"
description_url = "http://127.0.0.1:8600/describe_video"
image_by_pose_generator_url = "http://127.0.0.1:8500/generate_image_controlnet_pose"
image_by_face_generator_url = "http://127.0.0.1:8500/generate_image_controlnet_face"
image_by_inpaint_generator_url = "http://127.0.0.1:8500/generate_image_inpaint"


use_cases_app = FastAPI()


@use_cases_app.post('/request_thumbnail')
async def process_incoming_thumbnail_request(request: Request):
    
    logger.info("thumbnail")
    
    body_dict = await request.json()
    
    description_text = generate_video_description(body_dict["video"])
    prompt = generate_prompt(body_dict["title"], body_dict["description"], description_text)
    
    generated_image = generate_image_by_prompt(
        body_dict["lora_name"],
        prompt,
        "thumbnail"
    )
    upscaled_img = generate_upscaled_image(generated_image, "thumbnail")
    
    # TODO: POST to frontend
    
    logger.info("there is thumbnail image")


@use_cases_app.post('/request_incoming_profile_image_prompt')
async def process_incoming_profile_image_prompt(request: Request):
    
    body_dict = await request.json()
    
    prompt = translate(body_dict["prompt"])
    
    generated_image = generate_image_by_prompt(
        body_dict["lora_name"],
        prompt,
        "avatar"
    )
    
    upscaled_img = generate_upscaled_image(generated_image, "avatar")
    
    logger.info(generated_image)
    
    #TODO: POST to frontend
    
    logger.info("there is profile image by prompt")
    

@use_cases_app.post('/request_incoming_profile_image_body')
async def process_incoming_profile_image_body(request: Request):
    
    body_dict = await request.json()
    
    prompt = translate(body_dict["prompt"])
    
    generated_image = generate_image_by_pose(
        body_dict["lora_name"],
        prompt,
        body_dict["mask"],
        "avatar"
    )
    
    upscaled_img = generate_upscaled_image(generated_image, "avatar")
    
    logger.info(generated_image)
    
    #TODO: POST to frontend
    
    logger.info("there is profile image by body")

    
@use_cases_app.post('/request_incoming_profile_image_face')
async def process_incoming_profile_image_face(request: Request):
    
    body_dict = await request.json()
    
    prompt = translate(body_dict["prompt"])
    
    generated_image = generate_image_by_face(
        body_dict["lora_name"],
        prompt,
        body_dict["mask"],
        "avatar"
    )
    
    upscaled_img = generate_upscaled_image(generated_image, "avatar")
    
    #TODO: POST to frontend
    
    logger.info("there is profile image by face")
    
    
@use_cases_app.post('/request_incoming_profile_image_inpaint')
async def process_incoming_profile_image_inpaint(request: Request):
    
    body_dict = await request.json()
    
    prompt = translate(body_dict["prompt"])
    
    generated_image = generate_image_by_inpaint(
        body_dict["lora_name"],
        prompt,
        body_dict["orig_image"],
        body_dict["mask_image"],
        "avatar"
    )
    
    upscaled_img = generate_upscaled_image(generated_image, "avatar")
    
    #TODO: POST to frontend
    
    logger.info("there is profile image by inpaint")


@use_cases_app.post('/request_incoming_banner_prompt')
async def process_incoming_banner_prompt(request: Request):
    
    body_dict = await request.json()
    
    prompt = translate(body_dict["prompt"])
    
    generated_image = generate_image_by_prompt(
        body_dict["lora_name"],
        prompt,
        "banner"
    )
    
    upscaled_img = generate_upscaled_image(generated_image, "banner")
    
    logger.info(generated_image)
    
    #TODO: POST to frontend
    
    logger.info("there is banner by prompt")


@use_cases_app.post('/request_incoming_banner_body')
async def process_incoming_banner_body(request: Request):
    
    body_dict = await request.json()
    
    prompt = translate(body_dict["prompt"])
    
    generated_image = generate_image_by_pose(
        body_dict["lora_name"],
        body_dict["prompt"],
        body_dict["mask"],
        "banner"
    )
    
    upscaled_img = generate_upscaled_image(generated_image, "banner")
    
    logger.info(generated_image)
    
    #TODO: POST to frontend
    
    logger.info("there is banner by body")
    
    
@use_cases_app.post('/request_incoming_banner_face')
async def process_incoming_banner_face(request: Request):
    
    body_dict = await request.json()
    
    prompt = translate(body_dict["prompt"])
    
    generated_image = generate_image_by_face(
        body_dict["lora_name"],
        prompt,
        body_dict["mask"],
        "banner"
    )
    
    upscaled_img = generate_upscaled_image(generated_image, "banner")
    
    #TODO: POST to frontend
    
    logger.info("there is banner by face")
    
    
@use_cases_app.post('/request_incoming_banner_inpaint')
async def process_incoming_banner_inpaint(request: Request):
    
    body_dict = await request.json()
    
    prompt = translate(body_dict["prompt"])
    
    generated_image = generate_image_by_inpaint(
        body_dict["lora_name"],
        prompt,
        body_dict["orig_image"],
        body_dict["mask_image"],
        "banner"
    )
    
    upscaled_img = generate_upscaled_image(generated_image, "banner")
    
    #TODO: POST to frontend
    logger.info("there is banner by inpaint")
    


def generate_video_description(video):
    
    description_video_json = {
        "video": video
    }
    description_resp = requests.post(
        url=description_url,
        json=description_video_json
    )
    description_text = description_resp.json()
    description_text = description_text["video_description"]
    
    logger.info(description_text)
    
    return description_text
   

def generate_prompt(title, description, description_text):

    prompt_generator_payload = {
        "title": title,
        "description": description,
        "text": description_text
    }
    
    prompt_resp = requests.post(
        url=prompt_generator_url,
        json=prompt_generator_payload
    )
    prompt = prompt_resp.json()
    prompt = prompt["generated_prompt"]
    
    prompt = translate(prompt)
    
    return prompt


def generate_image_by_prompt(lora_name, prompt, task):
    
    prompt = translate(prompt)
    
    image_by_prompt_generator_payload = {
        "lora_name": lora_name,
        "prompt": prompt,
        "task": task
    }
    image_generation_resp = requests.post(
        url=image_by_prompt_generator_url,
        json=image_by_prompt_generator_payload
    )
    generated_image = image_generation_resp.json()
    generated_image = generated_image["generated_image"]
    
    logger.info(generated_image)
    
    return generated_image
 

def generate_upscaled_image(generated_image, type):
    
    image_to_upscale_payload = {
        "image_to_upscale": generated_image,
        "type": type
    }
    image_upscale_resp = requests.post(
        url=upscale_image_url,
        json=image_to_upscale_payload
    )
    image_upscale_resp = image_upscale_resp.json()
    image_upscale_resp = image_upscale_resp["upscaled_image"]
    
    logger.info(image_upscale_resp)
    
    return image_upscale_resp


def generate_image_by_pose(lora_file, prompt, pose_image, task):
    
    prompt = translate(prompt)

    pose_image_payload = {
        "lora_name": lora_file,
        "prompt": prompt,
        "task": task,
        "pose_image": pose_image
    }
    
    image_generation_resp = requests.post(
        url=image_by_pose_generator_url,
        json=pose_image_payload
    )
    generated_image = image_generation_resp.json()
    generated_image = generated_image["generated_image"]
    
    logger.info(generated_image)
    
    return generated_image


def generate_image_by_face(lora_file, prompt, face_image, task):

    prompt = translate(prompt)

    face_image_payload = {
        "lora_name": lora_file,
        "prompt": prompt,
        "task": task,
        "face_pose_image": face_image
    }
    
    image_generation_resp = requests.post(
        url=image_by_face_generator_url,
        json=face_image_payload
    )
    generated_image = image_generation_resp.json()
    generated_image = generated_image["generated_image"]
    
    logger.info(generated_image)
    
    return generated_image


def generate_image_by_inpaint(lora_file, prompt, orig_image, mask_image, task):

    prompt = translate(prompt)

    inpaint_image_payload = {
        "lora_name": lora_file,
        "prompt": prompt,
        "task": task,
        "orig_image": orig_image,
        "mask_image": mask_image
    }
    
    image_generation_resp = requests.post(
        url=image_by_inpaint_generator_url,
        json=inpaint_image_payload
    )
    generated_image = image_generation_resp.json()
    generated_image = generated_image["generated_image"]
    
    logger.info(generated_image)
    
    return generated_image


def translate(text_ru):
    payload = {
        "text": text_ru
    }

    resp = requests.post(
        url="http://127.0.0.1:8900/translate",
        json=payload
    )

    translated_text = resp.json()["translated_text"]
    
    return translated_text


async def main():
    config = uvicorn.Config(
        "use_cases_api:use_cases_app",
        port=8000,
        log_level="info",
        workers=6
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())