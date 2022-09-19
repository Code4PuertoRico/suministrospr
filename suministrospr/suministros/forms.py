import bleach
from django import forms
from django.conf import settings
from django.core.cache import cache
from django.utils.text import slugify
from django_select2.conf import settings as select2_settings
from django_select2.forms import Select2TagWidget

from .constants import ALLOWED_TAGS
from .models import Suministro, Tag


class TagsWidget(Select2TagWidget):
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
        attrs["data-minimum-input-length"] = 0
        return attrs

    def value_from_datadict(self, data, files, name):
        """
        Create objects for given non-pimary-key values. Return list of all primary keys.
        """
        values = set(super().value_from_datadict(data, files, name))

        # Numeric values are probably existing ids
        numeric_values = [int(value) for value in values if value.isdigit()]
        pks = Tag.objects.filter(**{"pk__in": numeric_values}).values_list(
            "pk", flat=True
        )

        # Convert ids to strings for set operation
        pks = set(map(str, pks))
        other_values = values - pks

        tag_ids = list(pks)

        for val in other_values:
            tag, _ = Tag.objects.get_or_create(name=slugify(val))
            tag_ids.append(tag.pk)

        return tag_ids


class SuministroModelForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by("name"), widget=TagsWidget, required=False
    )

    class Meta:
        model = Suministro
        fields = ["title", "municipality", "content", "tags"]

    def clean_content(self):
        content = self.cleaned_data["content"]
        return bleach.clean(content, tags=ALLOWED_TAGS, strip=True)


class FilterForm(forms.Form):
    tag = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["tag"].choices = [("", "---------")] + [
            (tag.slug, tag.name) for tag in cached_tags()
        ]


def cached_tags():
    cache_key = "forms:filter-tags"
    tags = cache.get(cache_key)
    if tags:
        return tags

    tags = Tag.objects.all().order_by("name")
    cache.set(cache_key, tags, settings.CACHE_MIXIN_TIMEOUT)
    return tags
