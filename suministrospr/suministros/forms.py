from django import forms

from .models import Suministro


class SuministroModelForm(forms.ModelForm):
    class Meta:
        model = Suministro
        fields = ["title", "municipality", "content"]
