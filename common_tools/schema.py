from pydantic import BaseModel


class BaseRequestSchema(BaseModel):
    prompt: str
    lora_name: str


class ThumbnailRequestSchema(BaseRequestSchema):
    type: str="thumbnail_request"
    title: str
    description: str
    

class ProfileImageRequestSchema(BaseRequestSchema):
    type: str="profile_image_request"
    mask: str #base64
    

class ChannelBannerRequestSchema(BaseRequestSchema):
    type: str="channel_banner_request"
    mask: str