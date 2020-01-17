import bleach
from django import forms
from django_select2.conf import settings as select2_settings
from django_select2.forms import ModelSelect2TagWidget

from .constants import ALLOWED_TAGS
from .models import Suministro, Tag


class TagsWidget(ModelSelect2TagWidget):
    model = Tag
    queryset = Tag.objects.all()
    search_fields = ["name__icontains"]
    empty_label = ""
    media = forms.Media(
        js=(select2_settings.SELECT2_JS,)
        + (f"{select2_settings.SELECT2_I18N_PATH}/es.js",)
        + ("django_select2/django_select2.js",),
        css={"screen": (select2_settings.SELECT2_CSS,)},
    )

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs["data-language"] = "es"
        return attrs

    def value_from_datadict(self, data, files, name):
        """
        Create objects for given non-pimary-key values. Return list of all primary keys.
        """
        values = set(super().value_from_datadict(data, files, name))
        numeric_values = [int(value) for value in values if value.isdigit()]
        pks = self.queryset.filter(**{"pk__in": numeric_values}).values_list(
            "pk", flat=True
        )
        pks = set(map(str, pks))
        cleaned_values = list(numeric_values)
        for val in values - pks:
            cleaned_values.append(self.queryset.create(name=val).pk)
        return cleaned_values


class SuministroModelForm(forms.ModelForm):
    class Meta:
        model = Suministro
        fields = ["title", "municipality", "content", "tags"]
        widgets = {"tags": TagsWidget}

    def clean_content(self):
        content = self.cleaned_data["content"]
        return bleach.clean(content, tags=ALLOWED_TAGS, strip=True)
