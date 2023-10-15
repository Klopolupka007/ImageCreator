import asyncio
import base64

from io import BytesIO
import uvicorn
from fastapi import FastAPI, Request
from PIL import Image
from upscaler_model import UpscaleModel

'''from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
from pyngrok import ngrok'''


upscale_model = UpscaleModel()

upscaler_app = FastAPI()

@upscaler_app.post('/upscale_image')
async def transcribe_video(request: Request):
    resp = await request.json()
    image_to_upscale = resp["image_to_upscale"]
    type_of_resp = resp["type"]
    
    if type_of_resp == "banner":
        w, h = 2204, 864
        
    elif type_of_resp == "thumbnail":
        w, h = 1280, 720
        
    elif type_of_resp == "avatar":
        w, h = 800, 800
    
    image_to_upscale = b64_to_pil(image_to_upscale)
    
    upscaled_image = upscale_model.upscale_image(image_to_upscale)
    upscaled_image = upscaled_image.resize((w, h))
    upscaled_image = image_to_base64(upscaled_image)

    return {"upscaled_image": upscaled_image}


def b64_to_pil(img_b64):
    decoded_image = base64.b64decode(img_b64)
    image_PIL = Image.open(BytesIO(decoded_image))
    
    return image_PIL


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    return image_base64


'''upscaler_app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)'''


async def main():
    config = uvicorn.Config(
        "upscaler_api:upscaler_app",
        port=8500,
        log_level="info",
        workers=6
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())