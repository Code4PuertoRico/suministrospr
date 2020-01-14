from django.db import models

from ckeditor.fields import RichTextField
from django_extensions.db.fields import AutoSlugField

from .constants import MUNICIPALITIES
from ..utils.models import BaseModel


class Suministro(BaseModel):
    MUNICIPALITY_CHOICES = [(value.lower(), value) for value in MUNICIPALITIES]

    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from=["title", "municipality"])
    municipality = models.CharField(max_length=255, choices=MUNICIPALITY_CHOICES)
    content = RichTextField()

    def __str__(self):
        return self.title
