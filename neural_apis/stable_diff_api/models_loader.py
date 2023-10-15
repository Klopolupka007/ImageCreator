import tomesd
import torch
from diffusers import StableDiffusionKDiffusionPipeline
from models.stable_diff_base_model import BaseModelWithPrompt
from models.stable_diff_body_pose_model import ControlNetBodyPose
from models.stable_diff_face_model import ControlNetFace
from models.stable_diff_inpaint_model import InpaintModel


def get_all_models():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    base_model = load_base_model(device)
    
    base_model_with_prompt = BaseModelWithPrompt(base_model, device)
    control_net_body_pose = ControlNetBodyPose(base_model_with_prompt, device)
    control_net_face = ControlNetFace(base_model_with_prompt, device)
    inpaint_model = InpaintModel(device)
    
    return {
        "base_model": base_model_with_prompt,
        "pose_model": control_net_body_pose,
        "face_model": control_net_face,
        "inpaint_model": inpaint_model
    }
    
    
def load_base_model(device):
    base_pipe = StableDiffusionKDiffusionPipeline.from_pretrained(
        "stablediffusionapi/realistic-vision-v51",
        torch_dtype=torch.float16
    ).to(device)
    
    base_pipe.set_scheduler('sample_dpmpp_2m')

    base_pipe = tomesd.apply_patch(base_pipe, ratio=0.5)
    base_pipe.enable_attention_slicing()
    
    return base_pipe