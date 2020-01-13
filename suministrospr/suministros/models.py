from django.db import models
from ckeditor.fields import RichTextField
from ..utils.models import BaseModel

MUNICIPALITY_CHOICES = []


class Suministro(BaseModel):
    title = models.CharField(max_length=255)
    municipality = models.CharField(max_length=255, choices=MUNICIPALITY_CHOICES)
    content = RichTextField()

    def __str__(self):
        return self.title
