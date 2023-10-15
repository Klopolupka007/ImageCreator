import asyncio

import uvicorn
from fastapi import FastAPI, Request
from prompt_translator import model, tokenizer


translator_app = FastAPI()

@translator_app.post('/translate')
async def translate(request: Request):
    req_body = await request.json()
    
    text_to_translate = req_body['text']
    
    text_en = translate(text_to_translate)
    
    return {"translated_text": text_en}


def translate(text_ru):
    encoded_ru = tokenizer(text_ru, return_tensors="pt")
    generated_tokens = model.generate(**encoded_ru)
    text_en = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    
    return text_en


async def main():
    config = uvicorn.Config(
        "translator_api:translator_app",
        port=8900,
        log_level="info",
        workers=6
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())