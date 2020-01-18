from django.db.models import Count, Prefetch
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from reversion.views import RevisionMixin

from ..utils.mixins import CacheMixin
from .constants import MUNICIPALITIES
from .forms import SuministroModelForm
from .models import Municipality, Suministro, Tag


class SuministroList(CacheMixin, ListView):
    model = Suministro
    cache_key = "suministro-list"

    def get_queryset(self):
        return Suministro.objects.all().defer("content").order_by("title")

    def get_context_data(self):
        data = super().get_context_data()

        municipalities_with_suministros = (
            Municipality.objects.all()
            .prefetch_related(
                Prefetch(
                    "suministros",
                    queryset=Suministro.objects.defer("content").order_by("title"),
                )
            )
            .annotate(suministro_count=Count("suministro"))
            .filter(suministro_count__gt=0)
            .order_by("-suministro_count")
        )

        data["sorted_results"] = [
            {
                "count": municipality.suministro_count,
                "municipality": municipality.name,
                "suministros": municipality.suministros.all(),
            }
            for municipality in municipalities_with_suministros
        ]

        data["tags"] = Tag.objects.all().order_by("name")

        return data


class SuministroByMunicipalityList(CacheMixin, ListView):
    model = Suministro
    template_name = "suministros/suministro_municipio_list.html"
    cache_key = "suministro-municipio-list"

    def get_cache_key(self):
        return f"{self.cache_key}:{self.kwargs['municipality']}"

    def get_queryset(self):
        return (
            Suministro.objects.select_related("municipality")
            .filter(municipality__slug=self.kwargs["municipality"])
            .defer("content")
            .order_by("title")
        )

    def get_context_data(self):
        data = super().get_context_data()
        data["municipality"] = MUNICIPALITIES.get(self.kwargs["municipality"])
        return data


class SuministroDetail(CacheMixin, DetailView):
    model = Suministro
    cache_key = "suministro-detail"

    def get_cache_key(self):
        return f"{self.cache_key}:{self.kwargs['slug']}"


class SuministroCreate(RevisionMixin, CreateView):
    model = Suministro
    form_class = SuministroModelForm

    def get_success_url(self):
        return reverse("suministro-detail", args=[self.object.slug])


class SuministroUpdate(RevisionMixin, UpdateView):
    model = Suministro
    form_class = SuministroModelForm

    def get_success_url(self):
        return reverse("suministro-detail", args=[self.object.slug])
