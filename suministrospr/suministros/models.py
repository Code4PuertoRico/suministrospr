import uuid

from ckeditor.fields import RichTextField
from django.core.cache import cache
from django.db import models
from django_extensions.db.fields import AutoSlugField

from ..utils.models import BaseModel
from .constants import MUNICIPALITIES


class Tag(BaseModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from=["name"], overwrite_on_add=False, max_length=255)

    def __str__(self):
        return self.name


class Suministro(BaseModel):
class Municipality(BaseModel):
    MUNICIPALITY_CHOICES = [(value, label) for value, label in MUNICIPALITIES.items()]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255, choices=MUNICIPALITY_CHOICES)
    slug = AutoSlugField(populate_from=["name"], overwrite_on_add=False, max_length=255)

    class Meta:
        verbose_name = "municipality"
        verbose_name_plural = "municipalities"

    def __str__(self):
        return self.name


class Suministro(BaseModel):
    MUNICIPALITY_CHOICES = [(value, label) for value, label in MUNICIPALITIES.items()]

    title = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from=["title", "municipality"], overwrite_on_add=False, max_length=255
    )
    municipality = models.CharField(max_length=255, choices=MUNICIPALITY_CHOICES)

    municipality_fk = models.ForeignKey(Municipality, null=True, default=None, on_delete=models.SET_NULL)

    tags = models.ManyToManyField(Tag, blank=True)

    content = RichTextField()

    class Meta:
        indexes = [models.Index(fields=["title"])]
        verbose_name = "suministro"
        verbose_name_plural = "suministros"

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
