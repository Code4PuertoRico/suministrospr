import bleach
from django import forms

from .constants import ALLOWED_TAGS
from .models import Suministro


class SuministroModelForm(forms.ModelForm):
    class Meta:
        model = Suministro
        fields = ["title", "municipality", "content"]

    def clean_content(self):
        content = self.cleaned_data["content"]
        return bleach.clean(content, tags=ALLOWED_TAGS, strip=True)
