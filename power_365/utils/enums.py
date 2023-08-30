from django.db import models
from django.utils.translation import gettext as _

# Enum for the different types of files
class MediaType(models.TextChoices):
    IMAGE = "image", _("image")
    VIDEO = "video", _("video")
    AUDIO = "audio", _("audio")
    DOCUMENT = "document", _("document")
    OTHER = "other", _("other")

