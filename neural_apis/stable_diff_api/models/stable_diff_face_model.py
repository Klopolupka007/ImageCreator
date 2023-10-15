import tomesd
import torch
from controlnet_aux import OpenposeDetector
from diffusers import (
    StableDiffusionControlNetPipeline,
    ControlNetModel,
    UniPCMultistepScheduler
)


class ControlNetFace:
    def __init__(self, base_model_with_prompt, device="cuda"):
        controlnet = ControlNetModel.from_pretrained(
            "CrucibleAI/ControlNetMediaPipeFace",
            subfolder="diffusion_sd15",
            torch_dtype=torch.float16
        )

        self.base_pipe = base_model_with_prompt

        self.pipeline = StableDiffusionControlNetPipeline(
            vae=self.base_pipe.pipeline.vae,
            text_encoder=self.base_pipe.pipeline.text_encoder,
            tokenizer=self.base_pipe.pipeline.tokenizer,
            unet=self.base_pipe.pipeline.unet,
            scheduler=self.base_pipe.pipeline.scheduler,
            feature_extractor=self.base_pipe.pipeline.feature_extractor,
            controlnet=controlnet,
            safety_checker=self.base_pipe.pipeline.safety_checker
        ).to(device)

        self.pipeline.scheduler = UniPCMultistepScheduler.from_config(
            self.pipeline.scheduler.config
        )

        self.pipeline = tomesd.apply_patch(
            self.pipeline,
            ratio=0.5
        )
        self.pipeline.enable_attention_slicing()

        self.openpose = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")


    def generate_image(self, pose_image, prompt, lora_filename=None, height=512, width=512):
        if lora_filename:
            self.base_pipe.load_lora(lora_filename)

        pose_image = self.openpose(pose_image)

        image = self.pipeline(
            prompt=prompt,
            negative_prompt=self.base_pipe.negative_prompt,
            image=pose_image,
            num_inference_steps=40,
            guidance_scale=8.,
            controlnet_conditioning_scale=0.9,
            width=width,
            height=height
        ).images[0]

        return image