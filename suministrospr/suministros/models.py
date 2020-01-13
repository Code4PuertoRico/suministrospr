from django.db import models
from ..utils.models import BaseModel

MUNICIPALITY_CHOICES = []


class Suministro(BaseModel):
    title = models.CharField(max_length=255)
    municipality = models.CharField(max_length=255, choices=MUNICIPALITY_CHOICES)
    content = models.TextField()

    def __str__(self):
        return self.title
