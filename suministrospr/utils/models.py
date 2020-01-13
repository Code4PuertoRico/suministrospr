from django.db import models

from .fields import DateTimeCreatedField, DateTimeModifiedField


class BaseModel(models.Model):
    created_at = DateTimeCreatedField()
    modified_at = DateTimeModifiedField()

    class Meta:
        get_latest_by = "modified_at"
        ordering = ("-modified_at", "-created_at")
        abstract = True
