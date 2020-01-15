from ckeditor.fields import RichTextField
from django.core.cache import cache
from django.db import models
from django_extensions.db.fields import AutoSlugField

from ..utils.models import BaseModel
from .constants import MUNICIPALITIES


class Suministro(BaseModel):
    MUNICIPALITY_CHOICES = [(value, label) for value, label in MUNICIPALITIES.items()]

    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from=["title", "municipality"])
    municipality = models.CharField(max_length=255, choices=MUNICIPALITY_CHOICES)
    content = RichTextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.invalidate_cache()

    def invalidate_cache(self):
        cache.delete_many(
            [
                "suministro-list",
                f"suministro-municipio-list:{self.municipality}",
                f"suministro-detail:{self.slug}",
            ]
        )
