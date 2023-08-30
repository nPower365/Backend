from uuid import uuid4
from config.settings.base import ALLOWED_AUDIO_TYPE, ALLOWED_DOCUMENT_TYPE, ALLOWED_IMAGE_TYPE, ALLOWED_VIDEO_TYPE

from power_365.utils.enums import MediaType

def generate_id(length: int = 8) -> str:
    return uuid4().hex

def get_media_type(extention: str) -> str:
    if extention.lower() in ALLOWED_IMAGE_TYPE:
        return MediaType.IMAGE
    elif extention.lower() in ALLOWED_VIDEO_TYPE:
        return MediaType.VIDEO
    elif extention.lower() in ALLOWED_AUDIO_TYPE:
        return MediaType.AUDIO
    elif extention.lower() in ALLOWED_DOCUMENT_TYPE:
        return MediaType.DOCUMENT
    else:
        return MediaType.OTHER

def is_image(filename: str) -> bool:
    import mimetypes
    try:
        return mimetypes.guess_type(filename)[0].startswith("image")
    except:
        return False
