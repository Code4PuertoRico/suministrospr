from django.db import models
from django.utils.timezone import now


class DateTimeCreatedField(models.DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("editable", False)
        kwargs.setdefault("default", now)
        super(DateTimeCreatedField, self).__init__(*args, **kwargs)


class DateTimeModifiedField(DateTimeCreatedField):
    def pre_save(self, model_instance, add):
        value = now()
        setattr(model_instance, self.attname, value)
        return value
