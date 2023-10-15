import asyncio

import requests
import uvicorn
from fastapi import FastAPI, Request
from Lama8GB import Generate, get_text


nlp_app = FastAPI()

@nlp_app.post('/generate_prompt')
async def request_profile_image(request: Request):
    req_body = await request.json()
    
    video_caption = req_body['text']
    
    text_ru = f"{req_body['title']} {req_body['description']}"
    
    text = f"{text_ru} \n {video_caption}"
    text = get_text(text)[0]
    prompt_ru = Generate(sentence=text)
    
    prompt = translate(prompt_ru)
    
    return {"generated_prompt": prompt}


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
        "nlp_api:nlp_app",
        port=8400,
        log_level="info",
        workers=6
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())