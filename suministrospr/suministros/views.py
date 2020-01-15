from collections import defaultdict

from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from reversion.views import RevisionMixin

from ..utils.mixins import CacheMixin
from .constants import MUNICIPALITIES
from .forms import SuministroModelForm
from .models import Suministro


class SuministroList(CacheMixin, ListView):
    model = Suministro
    cache_key = "suministro-list"

    def get_queryset(self):
        return Suministro.objects.all().defer("content").order_by("title")

    def get_context_data(self):
        data = super().get_context_data()
        items_by_municipality = defaultdict(lambda: {"count": 0, "items": []})

        # Group by `municipality`
        for suministro in data["object_list"]:
            key = suministro.get_municipality_display()
            items_by_municipality[key]["count"] += 1
            items_by_municipality[key]["items"].append(suministro)

        results = []

        # Convert to `dict` to `list` for sorting by count
        for municipality, result in items_by_municipality.items():
            results.append(
                {
                    "count": result["count"],
                    "suministros": result["items"],
                    "municipality": municipality,
                }
            )

        # Sort by municipalities with most items first.
        data["sorted_results"] = sorted(results, key=lambda k: k["count"], reverse=True)

        return data


class SuministroByMunicipalityList(CacheMixin, ListView):
    model = Suministro
    template_name = "suministros/suministro_municipio_list.html"
    cache_key = "suministro-municipio-list"

    def get_cache_key(self):
        return f"{self.cache_key}:{self.kwargs['municipality']}"

    def get_queryset(self):
        return (
            Suministro.objects.filter(municipality=self.kwargs["municipality"])
            .defer("content")
            .order_by("municipality", "title")
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
