import asyncio
import base64

from io import BytesIO
import uvicorn
from fastapi import FastAPI, Request
from video_description_model import VideoCaptioningModel

from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
from pyngrok import ngrok


video_captioning_model = VideoCaptioningModel()
video_description_app = FastAPI()

@video_description_app.post('/describe_video')
async def transcribe_video(request: Request):
    video_b64 = await request.json()
    video_b64 = video_b64["video"]
    
    out_filename = "./temp.mp4"
    save_b64_video(video_b64, out_filename)
    
    caption = video_captioning_model.get_caption(out_filename)
    
    return {"video_description": caption}


def save_b64_video(video_b64, out_filename):
    video_b64 = base64.b64decode(video_b64)
    video_b64 = BytesIO(video_b64)
    
    with open(out_filename, "wb") as f:
        f.write(video_b64.read())


video_description_app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

'''async def main():
    ngrok_tunnel = ngrok.connect(8600)
    print('Public URL:', ngrok_tunnel.public_url)
    nest_asyncio.apply()
    uvicorn.run(video_description_app, port=8600)
'''

async def main():
    config = uvicorn.Config(
        "video_description_api:video_description_app",
        port=8600,
        log_level="info",
        workers=6
    )
    server = uvicorn.Server(config)
    await server.serve()
    

if __name__ == "__main__":
    asyncio.run(main())