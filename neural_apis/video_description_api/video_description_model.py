import av
import numpy as np
import torch
from transformers import (
    AutoImageProcessor,
    AutoTokenizer,
    VisionEncoderDecoderModel
)


class VideoCaptioningModel:
    def __init__(self):
        self.image_processor = AutoImageProcessor.from_pretrained(
            "MCG-NJU/videomae-base",
            dtype=torch.float16
        )
        self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
        self.model = VisionEncoderDecoderModel.from_pretrained(
            "Neleac/timesformer-gpt2-video-captioning"
        ).to("cuda")


    def get_caption(self, video_path):

        container = av.open(video_path)

        # extract evenly spaced frames from video
        seg_len = container.streams.video[0].frames
        clip_len = self.model.config.encoder.num_frames
        indices = set(np.linspace(0, seg_len, num=clip_len, endpoint=False).astype(np.int64))
        frames = []
        container.seek(0)
        for i, frame in enumerate(container.decode(video=0)):
            if i in indices:
                frames.append(frame.to_ndarray(format="rgb24"))

        # generate caption
        gen_kwargs = {
            "min_length": 10,
            "max_length": 20,
            "num_beams": 8,
        }
        pixel_values = self.image_processor(frames, return_tensors="pt").pixel_values.to("cuda")
        tokens = self.model.generate(pixel_values, **gen_kwargs)
        caption = self.tokenizer.batch_decode(tokens, skip_special_tokens=True)[0]

        return caption