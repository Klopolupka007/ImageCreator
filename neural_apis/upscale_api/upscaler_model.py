import torch
from diffusers import StableDiffusionUpscalePipeline


class UpscaleModel:
    def __init__(self):
        self.pipeline = StableDiffusionUpscalePipeline.from_pretrained(
            "stabilityai/stable-diffusion-x4-upscaler",
            torch_dtype=torch.float16
        ).to("cuda")
        self.pipeline.enable_attention_slicing()


    def upscale_image(self, image):
        w, h = image.size
        w = int(w / 1.5)
        h = int(h / 1.5)
        image = image.resize((w, h))

        prompt = "hd 4k detailed super resolution high quality"

        upscaled_image = self.pipeline(
            prompt=prompt,
            image=image,
            num_inference_steps=30,
            num_images_per_prompt=1
        ).images[0]

        return upscaled_image