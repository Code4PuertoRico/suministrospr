import bleach
from django import forms

from .models import Suministro


ALLOWED_TAGS = [
    "div",
    "address",
    "a",
    "ul",
    "ol",
    "li",
    "h1",
    "h2",
    "h3",
    "h3",
    "h4",
    "h5",
    "h6",
    "p",
    "strong",
    "em",
    "u",
    "s",
    "br",
    "hr",
    "pre",
]


class SuministroModelForm(forms.ModelForm):
    class Meta:
        model = Suministro
        fields = ["title", "municipality", "content"]

    def clean_content(self):
        content = self.cleaned_data["content"]
        return bleach.clean(content, tags=ALLOWED_TAGS, strip=True,)
