import torch
from diffusers import StableDiffusionInpaintPipeline
from safetensors.torch import load_file
from collections import defaultdict


class InpaintModel:
    def __init__(self, device="cuda"):
        self.pipeline = StableDiffusionInpaintPipeline.from_pretrained(
            "runwayml/stable-diffusion-inpainting",
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16"
        ).to(device)

        self.pipeline.safety_checker = None

        self.values_of_last_lora = None
        self.device = device
        self.values_of_last_lora = None
        self.dtype = torch.float16

        self.negative_prompt = "deformed, blurry, disfigured, poorly drawn face, mutation, mutated, extra_limb, ugly, poorly drawn hands, fused fingers, messy drawing, broken legs, censored, censor_bar, mutated fingers, mutation, poorly drawn, black-white, bad anatomy, liquid body, liquidtongue, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, low res, bad shadow, fused breasts, bad breasts, poorly drawn breasts, extra breasts, liquid breasts, missingbreasts, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, fusedears, bad ears, poorly drawn ears, extra ears, liquid ears, heavy ears, missing ears, fused animal ears, bad animal ears, poorly drawn animal ears, extra animal ears, liquidanimal ears, heavy animal ears, missing animal ears, text, ui, error, missing fingers, missing limb, fused fingers, one hand with more than 5 fingers, one hand with less than 5 fingers, one hand with more than 5 digit, one hand with less than 5 digit, extra digit, fewer digits, fused digit, missing digit, bad digit, liquid digit, colorful tongue, blacktongue, cropped, watermark, username, blurry, JPEG artifacts, signature, malformed feet, extra feet, bad feet, poorly drawnfeet, fused feet, missing feet, extra shoes, bad shoes, fused shoes, more than two shoes, poorly drawn shoes, bad gloves, poorly drawn gloves, fused gloves, bad cum, poorly drawn cum, fused cum, bad hairs, poorly drawn hairs, fused hairs, ugly, bad face, fused face, poorly drawn face, cloned face, big face, long face, badeyes, fused eyes poorly drawn eyes, extra eyes, malformed limbs, more than 2 nipples, missing nipples, different nipples, fused nipples, bad nipples, poorly drawnnipples, black nipples, colorful nipples, short arm, (((missing arms))), missing thighs, missing calf, missing legs, mutation, duplicate, morbid, mutilated, poorly drawn hands, more than 1 left hand, more than 1 right hand, deformed, (blurry), disfigured, missing legs, extra arms, extra thighs, more than 2 thighs, extra calf,fused calf, extra legs, bad knee, extra knee, more than 2 legs, bad tails, bad mouth, fused mouth, poorly drawn mouth, bad tongue, tongue within mouth, too longtongue, black tongue, big mouth, cracked mouth, bad mouth, dirty face, dirty teeth, dirty pantie, fused pantie, poorly drawn pantie, fused cloth, poorly drawn cloth, badpantie, yellow teeth, thick lips, bad camel toe, colorful camel toe, bad asshole, poorly drawn asshole, fused asshole, missing asshole, bad anus, bad pussy, bad crotch, badcrotch seam, fused anus, fused pussy, fused anus, fused crotch, poorly drawn crotch, fused seam, poorly drawn anus, poorly drawn pussy, poorly drawn crotch, poorly drawn crotch seam, bad thigh gap, missing thigh gap, fused thigh gap, liquid thigh gap, poorly drawn thigh gap, poorly drawn anus, bad collarbone, fused collarbone, missing collarbone, liquid collarbone, worst quality, low quality, normal quality, liquid tentacles, bad tentacles, poorly drawn tentacles, split tentacles, fused tentacles, missing clit, bad clit, fused clit, colorful clit, black clit, liquid clit, QR code, bar code, censored, safety panties, safety knickers, beard, furry, pony, pubic hair, mosaic, futa, testis,more than 5 fingers,less than 5 fingers,more than 2 arms, (naked)"


    def load_lora(
        self,
        lora_filename,
        multiplier=0.7
    ):

        LORA_PREFIX_UNET = "lora_unet"
        LORA_PREFIX_TEXT_ENCODER = "lora_te"
        # load LoRA weight from .safetensors
        state_dict = load_file(
            lora_filename,
            device=self.device
        )

        values_to_add = []

        updates = defaultdict(dict)
        for key, value in state_dict.items():
            # it is suggested to print out the key, it usually will be something like below
            # "lora_te_text_model_encoder_layers_0_self_attn_k_proj.lora_down.weight"

            layer, elem = key.split('.', 1)
            updates[layer][elem] = value

        # directly update weight in diffusers model
        for i, (layer, elems) in enumerate(updates.items()):

            if "text" in layer:
                layer_infos = layer.split(LORA_PREFIX_TEXT_ENCODER + "_")[-1].split("_")
                curr_layer = self.pipeline.text_encoder
            else:
                layer_infos = layer.split(LORA_PREFIX_UNET + "_")[-1].split("_")
                curr_layer = self.pipeline.unet

            # find the target layer
            temp_name = layer_infos.pop(0)
            while len(layer_infos) > -1:
                try:
                    curr_layer = curr_layer.__getattr__(temp_name)
                    if len(layer_infos) > 0:
                        temp_name = layer_infos.pop(0)
                    elif len(layer_infos) == 0:
                        break
                except Exception:
                    if len(temp_name) > 0:
                        temp_name += "_" + layer_infos.pop(0)
                    else:
                        temp_name = layer_infos.pop(0)

            # get elements for this layer
            weight_up = elems['lora_up.weight'].to(self.dtype)
            weight_down = elems['lora_down.weight'].to(self.dtype)
            alpha = elems['alpha']
            if alpha:
                alpha = alpha.item() / weight_up.shape[1]
            else:
                alpha = 1.0

            # update weight
            if len(weight_up.shape) == 4:
                if (self.values_of_last_lora):
                    curr_layer.weight.data -= self.values_of_last_lora[i]

                val_to_add = multiplier * alpha * torch.mm(weight_up.squeeze(3).squeeze(2), weight_down.squeeze(3).squeeze(2)).unsqueeze(2).unsqueeze(3)
                curr_layer.weight.data += val_to_add

            else:
                if (self.values_of_last_lora):
                    curr_layer.weight.data -= self.values_of_last_lora[i]

                val_to_add = multiplier * alpha * torch.mm(weight_up, weight_down)
                curr_layer.weight.data += val_to_add

            values_to_add.append(val_to_add)

        self.values_of_last_lora = values_to_add[:]


    def generate_image(
        self,
        orig_img,
        mask_img,
        prompt,
        lora_filename=None,
        height=512,
        width=512
      ):
        if (lora_filename):
            self.load_lora(
                lora_filename,
                multiplier=0.7
            )

        res = self.pipeline(
            prompt=prompt,
            image=orig_img,
            mask_image=mask_img,
            strength=0.7,
            num_inference_steps=40,
            guidance_scale=7,
            negative_prompt=self.negative_prompt,
            width=width,
            height=height,
        ).images[0]

        return res