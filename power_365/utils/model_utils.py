import uuid
from django.db import models
from power_365.utils.utils import generate_id
from django.utils.translation import gettext_lazy as _

class BaseModelManager(models.Manager):
    """
    Base model manager for all models
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    # soft delete
    def delete(self, *args, **kwargs):
        self.model.is_active = False
        self.model.save()

class BaseModel(models.Model):
    """
    Base model for all models
    """
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True, serialize=False, verbose_name='ID')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    # custom manager
    objects = BaseModelManager()
    class Meta:
        ordering = ["-date_modified"]
        abstract = True
